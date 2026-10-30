"""Loopback-only teaching API. Never use this HTTP development server in production."""
import json
import threading
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
import jwt
from jwt import PyJWKClient
from jwt.exceptions import PyJWKClientConnectionError, PyJWKClientError

ROOT = Path(__file__).resolve().parent
TENANT = '2f3bd047-8146-4a8f-b7a9-f8f422392f6a'
API_ID = '487fb7d7-495e-4291-bf03-e0eba9367167'
CLIENT_ID = '529b206d-0fd4-4d9e-a31e-19a9e6177158'
ISSUER = f'https://login.microsoftonline.com/{TENANT}/v2.0'
ORIGIN = 'http://localhost:3000'
# Fixed trusted URL: no URLs from token headers are followed.
KEYS = PyJWKClient(f'https://login.microsoftonline.com/{TENANT}/discovery/v2.0/keys', lifespan=300, timeout=10)
INVENTORY = {'item': 'Gotham lab security tokens', 'quantity': 10, 'updates': 0}
LOCK = threading.Lock()

class Denied(Exception):
    def __init__(self, status, code, message):
        self.status, self.code, self.message = status, code, message

def validate_token(token):
    if not token or len(token) > 24000:
        raise Denied(401, 'invalid_token', 'A bearer access token is required.')
    try:
        header = jwt.get_unverified_header(token)
        if header.get('alg') != 'RS256' or not isinstance(header.get('kid'), str):
            raise jwt.InvalidTokenError('Unsupported signing header')
        key = KEYS.get_signing_key_from_jwt(token)
        key_issuer = key._jwk_data.get('issuer')
        if key_issuer and key_issuer.replace('{tenantid}', TENANT) != ISSUER:
            raise jwt.InvalidTokenError('Signing key issuer mismatch')
        claims = jwt.decode(token, key.key, algorithms=['RS256'], audience=API_ID,
                            issuer=ISSUER, leeway=0,
                            options={'require': ['exp', 'nbf', 'iat', 'aud', 'iss', 'tid', 'ver', 'sub', 'oid', 'azp']})
        if claims.get('tid') != TENANT or claims.get('ver') != '2.0':
            raise jwt.InvalidTokenError('Wrong tenant or token version')
        if not isinstance(claims.get('oid'), str) or not claims['oid']:
            raise jwt.InvalidTokenError('Missing delegated user')
        return claims
    except PyJWKClientConnectionError:
        raise Denied(503, 'signing_keys_unavailable', 'Could not retrieve Entra signing keys. Check internet access and retry.') from None
    except (jwt.InvalidTokenError, PyJWKClientError, ValueError, TypeError, KeyError):
        raise Denied(401, 'invalid_token', 'Token signature, lifetime, audience, issuer, or required claims failed validation.') from None

def authorize(claims, required_scope):
    if claims.get('azp') != CLIENT_ID:
        raise Denied(403, 'client_not_allowed', 'This API allows only the Gotham OAuth Client Lab application.')
    scopes = claims.get('scp')
    if not isinstance(scopes, str) or required_scope not in scopes.split():
        raise Denied(403, 'insufficient_scope', f'The token requires {required_scope}.')

def safe_claims(c):
    return {k: c.get(k) for k in ('ver', 'iss', 'aud', 'tid', 'azp', 'scp', 'exp')}

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # Never log headers, tokens, or authentication query strings.
    def reply(self, status, payload, extra=None):
        data = json.dumps(payload, indent=2).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Referrer-Policy', 'no-referrer')
        self.send_header('X-Content-Type-Options', 'nosniff')
        for k, v in (extra or {}).items(): self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)
    def do_GET(self): self.route()
    def do_POST(self): self.route()
    def route(self):
        # Exact Host/Origin checks limit DNS rebinding and cross-origin browser calls.
        if self.headers.get('Host') != 'localhost:3000':
            self.reply(400, {'error': 'Use http://localhost:3000/lab.html'}); return
        if self.headers.get('Origin') not in (None, ORIGIN):
            self.reply(403, {'error': 'origin_not_allowed'}); return
        path = urlsplit(self.path).path
        if path.startswith('/api/'):
            self.api(path); return
        files = {'/': ('index.html', 'text/html'), '/lab.html': ('lab.html', 'text/html'),
                 '/assets/app.js': ('assets/app.js', 'text/javascript'),
                 '/assets/bridge.js': ('assets/bridge.js', 'text/javascript')}
        if self.command != 'GET' or path not in files:
            self.reply(404, {'error': 'not_found'}); return
        filename, mime = files[path]
        data = (ROOT / filename).read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', mime+'; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Referrer-Policy', 'no-referrer')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers(); self.wfile.write(data)
    def api(self, path):
        request_id = str(uuid.uuid4())
        scope = 'Inventory.Read' if self.command == 'GET' else 'Inventory.Write'
        base = {'requestId': request_id, 'time': datetime.now(timezone.utc).isoformat(),
                'method': self.command, 'path': path, 'requiredScope': scope}
        if path != '/api/inventory':
            self.reply(404, {**base, 'error': 'not_found'}); return
        claims = None
        try:
            auth = self.headers.get('Authorization', '')
            pieces = auth.split()
            token = pieces[1] if len(pieces) == 2 and pieces[0].lower() == 'bearer' else ''
            claims = validate_token(token)
            authorize(claims, scope)
            with LOCK:
                if self.command == 'POST':
                    # Fixed, harmless in-memory operation; never write user input to disk.
                    INVENTORY['quantity'] += 1
                    INVENTORY['updates'] += 1
                inventory = dict(INVENTORY)
            self.reply(200, {**base, 'result': 'allowed', 'tokenValidation': 'passed',
                            'verifiedClaims': safe_claims(claims), 'inventory': inventory})
        except Denied as e:
            headers = {}
            if e.status == 401: headers['WWW-Authenticate'] = 'Bearer error="invalid_token"'
            if e.code == 'insufficient_scope':
                headers['WWW-Authenticate'] = f'Bearer error="insufficient_scope", scope="{scope}"'
            self.reply(e.status, {**base, 'result': 'denied', 'error': e.code, 'message': e.message,
                                 'tokenValidation': 'passed' if claims else 'not passed',
                                 **({'verifiedClaims': safe_claims(claims)} if claims else {})}, headers)

def main():
    try: server = ThreadingHTTPServer(('localhost', 3000), Handler)
    except OSError:
        raise SystemExit('Port 3000 is busy. Stop the Lab 11 server or other server and retry.')
    print('Gotham OAuth API Lab: http://localhost:3000/lab.html')
    print('Keep this window open. Stop with Ctrl+C. Internet access is needed for Entra signing keys.')
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()

if __name__ == '__main__': main()
