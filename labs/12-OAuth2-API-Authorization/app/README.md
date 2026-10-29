# Lab 12 — Gotham OAuth API Authorization

A local SPA acquires a Microsoft Entra access token using Authorization Code with PKCE. A Python API independently validates the token and enforces delegated scopes. No client secret is used.

## Start on Windows

1. Stop the Lab 11 server (Ctrl+C in its terminal). Both labs use port 3000.
2. Extract this ZIP into a new folder; do not run from inside the ZIP.
3. Install Python 3.11 or newer if needed. On first launch, internet access is required to install pinned Python packages.
4. Double-click `START-LAB.cmd`. This creates an isolated `.venv` in this folder and starts the local server.
5. Open **http://localhost:3000/lab.html** in Chrome. Keep the terminal window open.

On macOS/Linux: `python3 start_lab.py`, then open the same URL. Stop with Ctrl+C.

Node.js is not required to run this package. The MSAL bundles are included. To rebuild from source, install Node.js, run `npm ci`, then `npm run build` in this folder.

## Registration prerequisites

| Setting | Value |
| --- | --- |
| Tenant | `2f3bd047-8146-4a8f-b7a9-f8f422392f6a` |
| API app | Gotham OAuth API Lab |
| API client ID / expected audience | `487fb7d7-495e-4291-bf03-e0eba9367167` |
| Application ID URI | `api://487fb7d7-495e-4291-bf03-e0eba9367167` |
| API manifest | `api.requestedAccessTokenVersion: 2` |
| Exposed delegated scopes | `Inventory.Read`, `Inventory.Write` (admins only, enabled) |
| SPA client app | Gotham OAuth Client Lab |
| SPA client ID | `529b206d-0fd4-4d9e-a31e-19a9e6177158` |
| SPA redirect URI | `http://localhost:3000/` |
| Initial client permission | `Inventory.Read`, admin consent granted |
| Implicit access/ID tokens | Both unchecked |
| Allow public client flows | Disabled |

The root page is the MSAL v5 redirect bridge; the application is at `/lab.html`. Both app registrations must be in the same tenant. Any enterprise application assignment requirement must also be satisfied by the test user.

## Baseline tests — run before granting write

Sign in as the standard lab user, Dick Grayson, using **Sign in for Inventory.Read**. Complete any password/MFA prompts required by tenant policy. Do not infer fresh MFA from sign-in success alone.

| Button | Expected HTTP | Meaning |
| --- | --- | --- |
| Read inventory | 200 | Valid access token with Inventory.Read |
| Read without token | 401 | No bearer token |
| Read with tampered token | 401 | The app changes the signature of a copy of the access token |
| Test ID token rejection | 401 | The client ID token is not an access token for the API; wrong audience |
| Write with current token | 403 | Signature and claims are valid, but Inventory.Write is missing |

The write button intentionally sends the current token without acquiring another scope. A 403 response includes `tokenValidation: passed` and `insufficient_scope`. Confirm `scp` contains Inventory.Read and does not contain Inventory.Write for that baseline. If prior consent or an earlier write token exists, the baseline may already include write scope; record the actual result rather than claiming a 403.

Capture the API responses and history after the baseline. No raw token is displayed.

## Grant write and verify recovery

1. In Gotham OAuth Client Lab > API permissions, add the API's delegated **Inventory.Write** permission.
2. Grant admin consent for Gotham Labs.
3. Return to the app and click **Request read + write token**. Complete an interaction if prompted.
4. Click **Write with current token**. Expect HTTP 200 and `scp` containing Inventory.Write.
5. Confirm the fictional quantity increments. Updates are in memory and reset when the server stops.

Removing a permission later does not prove that an already-issued access token is revoked. This lab does not claim immediate revocation.

## What the API validates

The API uses PyJWT and cryptography, fixes the accepted algorithm to RS256, and retrieves public keys from a fixed tenant-specific Entra JWKS URL. It checks the signing-key issuer when supplied, token signature, exact v2 issuer, API audience, exp/nbf/iat, tenant ID, version, subject/user claim presence, allowed SPA client (`azp`), and exact space-delimited delegated scope (`scp`). It never follows token-supplied key URLs. A missing or invalid token is 401, a valid token without authorization is 403, and a signing-key network outage is 503.

The browser sends the access token in an Authorization bearer header to the same-origin API. Tokens are not included in URLs or response diagnostics. MSAL uses session storage; the app holds its current test token in memory. Response claims are selected from tokens accepted by the server. Raw tokens, credentials, codes, and verifiers are never logged by this app. Browser developer tools can still expose sensitive request data: do not publish raw tokens, authorization codes, code verifiers, or full network exports.

The server binds only to localhost, checks Host and browser Origin, exposes only four static files, and disables caching. It is a development HTTP server for a local lab, not a production API deployment. Production requires HTTPS, a production server, and operational controls.

## Validation performed before delivery

Twenty offline regression tests passed using disposable fixture RSA keys. They cover read/write authorization, missing/malformed tokens, invalid signatures, wrong audience/issuer/tenant/version, expiration, future validity times, missing claims, exact scope matching, wrong client, signing-key outage, key issuer mismatch, cross-origin requests, and source-file exposure. Run with `python -m unittest -v test_api.py` in an environment with the requirements installed.

These fixture tests are implementation checks. They are not evidence of a successful live Entra sign-in. Capture live lab results separately.

## Troubleshooting

- **Port 3000 busy:** stop the old lab server; keep the registered redirect URI unchanged.
- **Python packages fail to install:** verify Python 3.11+, internet access, and any proxy settings. Keep the error message for troubleshooting.
- **AADSTS50105:** the account is not assigned to an enterprise application requiring assignment. Verify the exact app and test account.
- **Admin approval:** verify the client has admin consent for the exact scope requested. The write stage intentionally needs additional admin consent.
- **interaction_in_progress:** finish or close Microsoft popup windows before another interaction. Only after that error, the next interactive retry uses MSAL's recovery override.
- **401 after sign-in:** check API manifest version 2, API audience, system clock, and exact registration IDs. A client ID token is deliberately rejected.
- **503 signing_keys_unavailable:** check internet access to login.microsoftonline.com and retry.
- **No password/MFA prompt after clearing cache:** the Microsoft browser session can remain active; cache clearing is not Entra logout.
- **Popup warning about Cross-Origin-Opener-Policy:** inspect whether the operation actually completed. This server does not add a COOP header.

## Dependencies and sources

- Bundled: Microsoft MSAL Browser 5.27.0, built with esbuild 0.25.12. Included license notices are in `licenses/`.
- Runtime: Python 3.11+, PyJWT[crypto] 2.15.1, cryptography 50.0.2; installed into `.venv`. Transitive runtime dependencies are resolved by pip.
- https://learn.microsoft.com/en-us/entra/identity-platform/claims-validation
- https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens
- https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-configure-app-access-web-apis
- https://pyjwt.readthedocs.io/en/stable/usage.html
