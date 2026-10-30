"""Offline security regression tests using disposable fixture keys, not Entra evidence."""
import copy
import http.client
import json
import threading
import time
import unittest
from unittest.mock import patch
from types import SimpleNamespace
from cryptography.hazmat.primitives.asymmetric import rsa
import jwt
import server

class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.private = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        cls.public = cls.private.public_key()
        cls.other = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        cls.httpd = server.ThreadingHTTPServer(('localhost', 0), server.Handler)
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown(); cls.httpd.server_close(); cls.thread.join()
    def claims(self):
        now=int(time.time())
        return dict(iss=server.ISSUER,aud=server.API_ID,tid=server.TENANT,azp=server.CLIENT_ID,
                    ver='2.0',sub='fixture-subject',oid='fixture-user',iat=now,nbf=now-1,exp=now+600,scp='Inventory.Read')
    def token(self, changes=None, remove=None, other=False):
        c=self.claims(); c.update(changes or {})
        for k in remove or []: c.pop(k,None)
        return jwt.encode(c,self.other if other else self.private,algorithm='RS256',headers={'kid':'fixture-key'})
    def call(self, token=None, method='GET', origin=None, host='localhost:3000'):
        headers={'Host':host}
        if token is not None: headers['Authorization']='Bearer '+token
        if origin: headers['Origin']=origin
        conn=http.client.HTTPConnection('localhost',self.httpd.server_port,timeout=3)
        with patch.object(server.KEYS,'get_signing_key_from_jwt',return_value=SimpleNamespace(key=self.public,_jwk_data={'issuer':server.ISSUER})):
            conn.request(method,'/api/inventory',headers=headers)
            r=conn.getresponse(); status=r.status; payload=json.loads(r.read());conn.close()
        return status,payload
    def test_read_allowed(self):
        status,p=self.call(self.token());self.assertEqual(status,200);self.assertEqual(p['tokenValidation'],'passed');self.assertNotIn('oid',p['verifiedClaims'])
    def test_missing_and_malformed(self):
        for token in (None,'not-a-token'):
            with self.subTest(token=token):self.assertEqual(self.call(token)[0],401)
    def test_tampered_signature(self):self.assertEqual(self.call(self.token(other=True))[0],401)
    def test_wrong_audience_including_client_id_token(self):self.assertEqual(self.call(self.token({'aud':server.CLIENT_ID}))[0],401)
    def test_wrong_issuer(self):self.assertEqual(self.call(self.token({'iss':'https://attacker.invalid'}))[0],401)
    def test_wrong_tenant(self):self.assertEqual(self.call(self.token({'tid':'other-tenant'}))[0],401)
    def test_wrong_version(self):self.assertEqual(self.call(self.token({'ver':'1.0'}))[0],401)
    def test_expired(self):self.assertEqual(self.call(self.token({'exp':int(time.time())-1}))[0],401)
    def test_future_nbf(self):self.assertEqual(self.call(self.token({'nbf':int(time.time())+600}))[0],401)
    def test_future_iat(self):self.assertEqual(self.call(self.token({'iat':int(time.time())+600}))[0],401)
    def test_missing_required_claims(self):
        for claim in ('exp','nbf','iat','aud','iss','tid','ver','sub','oid','azp'):
            with self.subTest(claim=claim):self.assertEqual(self.call(self.token(remove=[claim]))[0],401)
    def test_other_client_forbidden(self):self.assertEqual(self.call(self.token({'azp':'other-client'}))[0],403)
    def test_write_denied_without_modifying_inventory(self):
        before=copy.deepcopy(server.INVENTORY);status,p=self.call(self.token(),method='POST')
        self.assertEqual(status,403);self.assertEqual(p['error'],'insufficient_scope');self.assertEqual(p['tokenValidation'],'passed');self.assertEqual(server.INVENTORY,before)
    def test_scope_must_match_exactly(self):self.assertEqual(self.call(self.token({'scp':'Inventory.ReadExtra'}))[0],403)
    def test_no_delegated_scope(self):self.assertEqual(self.call(self.token(remove=['scp']))[0],403)
    def test_write_allowed(self):
        before=server.INVENTORY['updates'];status,p=self.call(self.token({'scp':'Inventory.Read Inventory.Write'}),method='POST');self.assertEqual(status,200);self.assertEqual(p['inventory']['updates'],before+1)
    def test_bad_origin_and_host(self):
        self.assertEqual(self.call(origin='https://attacker.invalid')[0],403);self.assertEqual(self.call(host='attacker.invalid')[0],400)
    def test_signing_key_outage(self):
        with patch.object(server.KEYS,'get_signing_key_from_jwt',side_effect=server.PyJWKClientConnectionError('offline')):
            with self.assertRaises(server.Denied) as error:server.validate_token(self.token())
        self.assertEqual(error.exception.status,503)
    def test_wrong_key_issuer(self):
        with patch.object(server.KEYS,'get_signing_key_from_jwt',return_value=SimpleNamespace(key=self.public,_jwk_data={'issuer':'https://wrong.invalid'})):
            with self.assertRaises(server.Denied) as error:server.validate_token(self.token())
        self.assertEqual(error.exception.status,401)
    def test_static_server_does_not_expose_source(self):
        conn=http.client.HTTPConnection('localhost',self.httpd.server_port)
        conn.request('GET','/server.py',headers={'Host':'localhost:3000'});r=conn.getresponse();self.assertEqual(r.status,404);r.read();conn.close()

if __name__=='__main__':unittest.main(verbosity=2)
