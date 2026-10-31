import os
from functools import wraps
from pathlib import Path
from urllib.parse import urlencode

from dotenv import load_dotenv
from flask import Flask, abort, redirect, render_template_string, request, session, url_for
import msal

load_dotenv(Path(__file__).with_name('.env'))
TENANT_ID = os.getenv('TENANT_ID', '').strip()
CLIENT_ID = os.getenv('CLIENT_ID', '').strip()
CLIENT_SECRET = os.getenv('CLIENT_SECRET', '').strip()
SESSION_SECRET = os.getenv('SESSION_SECRET', '').strip()
REDIRECT_URI = os.getenv('REDIRECT_URI', 'http://localhost:5000/auth/callback').strip()
if not SESSION_SECRET:
    raise RuntimeError('Set SESSION_SECRET in .env before running')
app = Flask(__name__)
app.secret_key = SESSION_SECRET
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax')
SCOPES = ['User.Read']

PAGE = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Gotham Access Lab</title><style>body{font:16px system-ui,sans-serif;max-width:900px;margin:35px auto;padding:0 20px;line-height:1.6;color:#17212f}nav{display:flex;flex-wrap:wrap;gap:15px}a{color:#1558a0}pre{background:#f1f4f7;padding:18px;overflow:auto;border-radius:8px} .status{padding:12px;background:#edf3fa;border-radius:8px}</style></head><body><h1>Gotham Access Lab</h1><nav><a href="/">Home</a><a href="/whoami">Identity</a><a href="/it">IT Inventory</a><a href="/procurement">Procurement</a>{% if user %}<a href="/logout">Sign out</a>{% else %}<a href="/login">Sign in with Entra ID</a>{% endif %}</nav><hr>{% if user %}<p class="status">Signed in as {{user.get('name') or user.get('preferred_username') or 'User'}}</p>{% endif %}<h2>{{heading}}</h2><p>{{message}}</p>{% if data %}<pre>{{data}}</pre>{% endif %}</body></html>'''

def msal_client():
    if not all([TENANT_ID, CLIENT_ID, CLIENT_SECRET]):
        raise RuntimeError('Configure TENANT_ID, CLIENT_ID, CLIENT_SECRET in .env')
    return msal.ConfidentialClientApplication(CLIENT_ID, authority=f'https://login.microsoftonline.com/{TENANT_ID}', client_credential=CLIENT_SECRET)

def page(heading, message='', data=None, status=200):
    return render_template_string(PAGE, heading=heading, message=message, data=data, user=session.get('user')), status

def signin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return fn(*args, **kwargs)
    return wrapper

@app.get('/')
def index():
    return page('Application access testing', 'Test Entra app-role authorization using the links above. Roles are taken from validated ID token claims, not from local group names.')

@app.get('/login')
def login():
    flow = msal_client().initiate_auth_code_flow(SCOPES, redirect_uri=REDIRECT_URI)
    session['auth_flow'] = flow
    return redirect(flow['auth_uri'])

@app.get('/auth/callback')
def auth_callback():
    flow = session.pop('auth_flow', None)
    if not flow:
        return page('Authentication error', 'Missing or expired login state. Start sign-in again.', status=400)
    try:
        result = msal_client().acquire_token_by_auth_code_flow(flow, request.args)
    except ValueError:
        return page('Authentication error', 'Invalid authentication state or response.', status=400)
    if 'error' in result:
        return page('Authentication error', str(result.get('error_description', result['error'])), status=403)
    claims = result.get('id_token_claims')
    if not claims:
        return page('Authentication error', 'No validated ID token claims were returned.', status=403)
    session.clear()
    session['user'] = {key: claims.get(key) for key in ('name','preferred_username','oid','tid','roles')}
    return redirect(url_for('whoami'))

@app.get('/whoami')
@signin_required
def whoami():
    import json
    return page('Identity and role claims', 'Roles from Microsoft Entra ID token:', json.dumps(session['user'], indent=2))

@app.get('/it')
@signin_required
def it():
    if 'IT.Reader' not in (session['user'].get('roles') or []):
        return page('Forbidden', 'IT Inventory: no IT.Reader application role.', status=403)
    return page('IT Inventory', 'IT Reader access allowed.')

@app.get('/procurement')
@signin_required
def procurement():
    if 'Procurement.Reader' not in (session['user'].get('roles') or []):
        return page('Forbidden', 'Procurement: no Procurement.Reader application role.', status=403)
    return page('Procurement', 'Procurement Reader access allowed.')

@app.get('/logout')
def logout():
    session.clear()
    post = url_for('index', _external=True)
    return redirect('https://login.microsoftonline.com/' + (TENANT_ID or 'organizations') + '/oauth2/v2.0/logout?' + urlencode({'post_logout_redirect_uri':post}))

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False)
