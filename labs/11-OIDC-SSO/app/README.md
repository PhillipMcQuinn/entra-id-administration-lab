# Gotham OIDC Lab — Lab 11 Test Application

This is the test application, not a record of completed lab results.

## Run on Windows

1. Extract the ZIP to a folder.
2. Double-click START-LAB.cmd (requires Python 3).
3. Keep the console open and visit http://localhost:3000/lab.html in Chrome or Edge Incognito.
4. Allow the Microsoft sign-in popup for this localhost site.

If the launcher cannot find `py`, open a terminal in the extracted folder and run `python start_lab.py`.
No Node installation, pip installation, client secret, or build step is needed to run the prebuilt application. Internet access to Microsoft sign-in endpoints is required.

## Entra configuration

- Name: Gotham OIDC Lab
- Client: 0ab52627-9b78-4bb9-b721-82916d824e69
- Tenant: 2f3bd047-8146-4a8f-b7a9-f8f422392f6a
- Supported account types: this organizational directory only
- Platform: SPA
- Redirect URI: http://localhost:3000/ (the root is the dedicated MSAL v5 redirect bridge)
- Start page: http://localhost:3000/lab.html
- Implicit access-token and ID-token grants: off
- Allow public client flows: leave disabled
- Enterprise application: assignment required = Yes
- Initial test: Dick Grayson remains unassigned

The launch page and authentication callback are intentionally different. Keep the existing root redirect URI; do not replace it with /lab.html for login. Leave /unregistered-callback.html unregistered for the deliberate mismatch test.

## Testing sequence

1. Capture initial unassigned-user denial (expected AADSTS50105).
2. Assign Dick Grayson, then repeat sign-in and capture actual result.
3. Inspect selected ID-token claims. App roles appear only if defined, assigned, and issued; absence is displayed rather than treated as failure.
4. In developer tools, inspect only authorization-request parameters: response_type=code, code_challenge_method=S256, and presence of code_challenge/state/nonce. Do not publish codes, verifier, raw tokens, or network exports. PKCE is provided by MSAL; it is not proven by the page's static library label.
5. After a baseline success, run the unregistered-redirect test (expected AADSTS50011). Capture the Microsoft error, close the popup, then use normal sign-in to verify recovery. Do not fix this deliberate test by registering its callback.
6. Compare Clear this app’s cache with Sign out through Entra. Observe actual sign-in behavior afterward; do not assume clearing the local cache ends Microsoft's session.
7. Remove assignment and test a fresh sign-in. Record existing-session behavior separately.

## Implementation and limitations

Uses Microsoft MSAL Browser 5.27.0, Authorization Code flow with PKCE and popup interaction. OpenID scopes only are requested by application code; no Graph API call is implemented. MSAL may add its standard OIDC scopes. Tokens are managed by MSAL using session storage. Raw tokens are not rendered/exported or sent to the Python server by application code. Only selected claims are shown; subject, object ID and nonce are masked. MSAL diagnostics with potential PII are not logged.

The displayed audience, issuer, tenant, subject and expiry checks are teaching comparisons. They do not constitute independent cryptographic signature verification. This browser demo does not implement a protected API or server-side role enforcement. Do not use its UI as a production authorization boundary.

The Python server binds only to localhost. No COOP header is added to the bridge page. Retest actual Entra sign-in in your tenant; the package's local build does not establish end-to-end authentication success.

## Source and rebuild

Source files and package-lock.json are included. To rebuild after installing Node.js, run `npm ci` then `npm run build`. Dependency licenses are included with the distribution.

References:
- https://learn.microsoft.com/en-us/entra/msal/javascript/browser/about-msal-browser
- https://learn.microsoft.com/en-us/entra/msal/javascript/browser/redirect-bridge
- https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow

## Logout recovery update

Logout keeps the main page open until MSAL completes its cleanup. If a previous popup left `interaction_in_progress`, close Microsoft popups and click Sign in again. After this specific error, the next explicit click uses MSAL's popup recovery option to cancel the stale interaction. It does not establish that server logout succeeded.
