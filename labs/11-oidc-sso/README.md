# Lab 11 — OpenID Connect SSO with Authorization Code and PKCE

**Lab date:** October 29, 2026. **Licensing:** Microsoft Entra ID P2 free trial. Results reflect testing during the active trial.

I configured a single-tenant Microsoft Entra ID sign-in integration for a local browser application. I validated ID-token claim comparisons, captured an authorization request using PKCE, resolved consent and redirect failures, compared local-cache clearing with Entra logout, and verified that removing an assignment blocks a new sign-in.

**Environment:** personal GothamLabz Entra ID P2 tenant · **Test date:** October 29, 2026 · **Test identity:** fictional employee Dick Grayson. I performed all administration and testing myself, using my administrator account for configuration and Dick Grayson's account for user access tests. P2 describes the lab environment; OIDC and PKCE are not presented as P2-only features.

## Configuration

| Setting | Recorded configuration |
|---|---|
| Application | Gotham OIDC Lab |
| Application/client ID | `0ab52627-9b78-4bb9-b721-82916d824e69` |
| Tenant ID | `2f3bd047-8146-4a8f-b7a9-f8f422392f6a` |
| App registration object ID | `2eb6bdc2-017a-47df-98e5-6763ba232292` |
| Enterprise application object ID | `9b0fb696-94ad-4028-b75e-7383a2dab44c` |
| Supported accounts | This organization only |
| Platform and registered redirect | Single-page application; `http://localhost:3000/` |
| Application page | `http://localhost:3000/lab.html` |
| Authentication library | Microsoft MSAL Browser 5.27.0 |
| Flow | Authorization Code with PKCE; popup sign-in |
| Implicit access/ID token grants | Both unchecked |
| Allow public client flows | Disabled |
| Client secret | None used |
| Token cache | Session storage |
| Final delegated scopes with admin consent | `openid`, `profile`, `offline_access` |
| Assignment required | Yes |
| Visible to users | No |

The root page is a dedicated MSAL redirect bridge; the interactive lab page is `lab.html`. The registered redirect remains the root URL. The application explicitly requests `openid profile`; the captured authorization request also includes `offline_access`.

## Test Results

| Test | Observed outcome |
|---|---|
| Initial unassigned sign-in | Entra rejected Dick with **AADSTS50105** |
| Assigned sign-in before consent correction | **Need admin approval** page |
| Consent configuration | I removed default delegated `User.Read`, configured `openid`, `profile`, `offline_access`, and granted administrator consent |
| Successful sign-in | Application displayed Dick's identity; MSAL completed with `fromCache: false` |
| Claim comparisons | Audience, issuer, tenant, future expiry, and subject-presence checks all PASS |
| PKCE inspection | `/oauth2/v2.0/authorize` request showed `response_type=code`, a `code_challenge`, and `code_challenge_method=S256` |
| Deliberate redirect mismatch | Unregistered callback rejected with **AADSTS50011** |
| Redirect recovery | Normal sign-in succeeded using the registered root redirect |
| Clear local app cache | I cleared the app account/claim display and signed in again without a password or MFA prompt |
| Entra logout | After logout through the updated app, I entered a password and completed MFA on the next sign-in |
| Assignment removal | I removed Dick's assignment and retained my administrator account's assignment |
| New sign-in after removal and cache clearing | Entra rejected Dick again with **AADSTS50105** |

## Implementation and Claim Inspection

The browser application uses MSAL's public-client popup APIs without a client secret. It displays selected ID-token claims and masks `sub`, `oid`, and `nonce`. It does not display raw tokens.

The five PASS checks compare `aud` with the client ID, `iss` with the tenant v2 issuer, `tid` with the configured tenant, `exp` with the current clock, and confirm that `sub` is present. These are **teaching comparisons, not independent cryptographic signature validation**. I found no application roles in the inspected token and did not test custom app-role authorization in this lab. The application makes no Microsoft Graph API call.

![Successful sign-in and claim comparisons](screenshots/07-sign-in-claims.png)

## Troubleshooting

### Assignment and consent are separate controls

My initial sign-in attempt as the unassigned Dick Grayson account failed with AADSTS50105. After I assigned the account, the next attempt reached an administrator-approval requirement. I reviewed the API permissions, which initially showed delegated `User.Read`, then configured the three OIDC scopes and granted consent for Gotham Labs. I signed in successfully after this change. This sequence does not establish that `User.Read` inherently requires administrator consent in every tenant.

![Initial assignment denial](screenshots/04-initial-unassigned-denial.png)
![Administrator approval required](screenshots/05-admin-approval-required.png)
![Final granted scopes](screenshots/06-oidc-consent-granted.png)

### Redirect URI mismatch

I used the test button to request `http://localhost:3000/unregistered-callback.html`, which I deliberately left out of the registration. Entra returned AADSTS50011. I returned to normal sign-in with `http://localhost:3000/` and authenticated successfully without registering the bad callback.

![Redirect mismatch](screenshots/08-redirect-mismatch.jpg)
![Successful recovery](screenshots/09-redirect-recovery.png)

### Logout and stale interaction state

The original app's logout navigated the main page before MSAL finished interaction cleanup. My next sign-in attempt returned `interaction_in_progress`, and refreshing did not resolve it. The app was updated to keep the main page open until popup logout completes. A retry after this specific error uses MSAL's `overrideInteractionInProgress` option on the next explicit sign-in click, after closing Microsoft popups. This is recovery for a stale client operation, not a bypass of Entra authentication or assignment checks.

After the app update, I completed sign-in successfully. I retested logout and encountered password and MFA prompts on the next sign-in.

![Stale interaction error](screenshots/12-interaction-in-progress.png)
![Recovery after app update](screenshots/13-updated-app-recovery.png)
![Logout returned](screenshots/14-logout-returned.png)

## Cache and Session Findings

Clearing this application's MSAL cache does not itself request server logout. During my cache test, I signed in again without a password or MFA prompt. After Entra logout through the corrected app, I entered my password and completed MFA.

**Evidence distinction:** the matching successful Entra event at **20:19:32 UTC** records MFA as **Previously satisfied / MFA requirement satisfied by claim in the token**. Its correlation ID matches the application's Latest operation: `01a18950-cc3f-71a4-9332-b70c8e9009ce`. I observed the password and MFA prompts directly, but this log does not independently establish a fresh MFA challenge for that event. The earlier 20:04:41 UTC event also recorded previously satisfied factors.

![Local cache cleared](screenshots/10-app-cache-cleared.png)
![Successful sign-in after cache clearing](screenshots/11-cache-sign-in.png)
![Matching application operation](screenshots/15-matching-app-operation.png)
![Entra success event](screenshots/16-matching-entra-success.png)
![Authentication details](screenshots/17-authentication-details.png)

## Protocol Evidence

I inspected the Microsoft sign-in popup's Network panel and reloaded the account-picker page to capture the authorization request. Its parameters show the configured client, tenant endpoint, root redirect, OIDC scopes, `response_type=code`, a PKCE challenge, and `S256`. This confirms that the captured authorization request requested Authorization Code with PKCE. I did not independently capture the token exchange or verifier comparison.

![Authorization request with PKCE](screenshots/18-pkce-authorization-request.png)

I excluded raw token responses, authorization codes, code verifiers, cookies, and full network exports from the published evidence.

## Access Removal and Final State

I captured the assigned-user list, removed Dick's assignment, cleared the app cache, and attempted a new sign-in as Dick. Entra returned AADSTS50105. I retained **Assignment required = Yes** and **Visible to users = No**, along with my administrator account's assignment.

![Assigned users before removal](screenshots/19-assigned-users.png)
![Dick removed, Phillip retained](screenshots/20-assignment-removed.png)
![New sign-in denied after removal](screenshots/21-post-removal-denial.png)
![Final properties](screenshots/22-final-properties.png)

This validates denial of a **new authorization attempt** after removal. I did not test immediate revocation of previously issued tokens or termination of an existing application session. After testing, I closed the popup and stopped the local server. I retained the app registration and administrator consent.

## Reproduce the Local Application

The [app directory](app/) includes source, pinned dependency manifests, prebuilt browser bundles, Microsoft library licenses, a localhost Python server, and a Windows launcher. Python 3 is needed to run it; Node.js is needed only to rebuild the bundles.

1. Review the client and tenant IDs in `app/src/app.js` for your own lab registration.
2. Configure the root redirect as a SPA URI and keep implicit grants off.
3. Run `START-LAB.cmd` on Windows, or `python start_lab.py` from the app directory.
4. Open `http://localhost:3000/lab.html`.
5. Stop the server with Ctrl+C after testing.

See [application instructions](app/README.md) for setup and diagnostic details. This is a training application, not a production authorization service.

## Configuration Evidence

![App registration](screenshots/01-app-registration.png)
![SPA redirect](screenshots/02-spa-redirect.png)
![Implicit grants and public client settings](screenshots/03-authentication-settings.png)

## Skills Demonstrated

- Configure an Entra SPA registration and enterprise application assignment requirements.
- Diagnose assignment, consent, redirect, and client interaction errors separately.
- Inspect ID-token claims and verify an authorization request's PKCE parameters.
- Compare application cache state with identity-provider session behavior.
- Correlate application diagnostics with Entra logs and document evidence limits.
- Validate new-sign-in denial after access removal.

## References

- [MSAL Browser sign-in and popup recovery](https://learn.microsoft.com/en-us/entra/msal/javascript/browser/login-user)
- [MSAL Browser errors](https://learn.microsoft.com/en-us/entra/msal/javascript/browser/errors)
- [MSAL redirect bridge](https://learn.microsoft.com/en-us/entra/msal/javascript/browser/redirect-bridge)
- [MSAL resources and scopes](https://learn.microsoft.com/en-us/entra/msal/javascript/browser/resources-and-scopes)

[Return to portfolio](../../README.md)
