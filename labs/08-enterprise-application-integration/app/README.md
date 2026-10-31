# Gotham Access Lab — Local Flask/OIDC Application

I used this recreated demonstration application to test Microsoft Entra sign-in and the `IT.Reader` and `Procurement.Reader` application roles. I added the source to this repository after completing Labs 14 and 15. It comes from the restored application package used for those exercises; it is not a byte-for-byte recovery of the earlier original application.

## Files

| File | Purpose |
|---|---|
| `app.py` | Flask routes, MSAL sign-in, role checks, and sign-out |
| `requirements.txt` | Python dependency ranges |
| `.env.example` | Configuration template with placeholder secrets |
| `.gitignore` | Excludes `.env`, the virtual environment, and Python cache files |

## Entra prerequisites

I used a single-tenant **Gotham Access Lab** app registration and its enterprise application. To reproduce this in another tenant, use that tenant's identifiers and assignments.

1. Configure a **Web** platform with redirect URI `http://localhost:5000/auth/callback`.
2. Define enabled application roles for **Users/Groups** with values `IT.Reader` and `Procurement.Reader`.
3. Assign the appropriate users or security groups to each corresponding role under **Enterprise applications → Users and groups**. Set **Assignment required? → Yes** to reproduce the unassigned-user denial.
4. The application requests delegated Microsoft Graph `User.Read`. Configure that permission and obtain administrator consent where required by the tenant's consent policy. The code does not call a Graph endpoint; its authorization checks use the ID token's roles claim.
5. Create a client secret and privately copy its **Value**, then configure it locally. The example client ID identifies my lab registration; replace it when using your own registration.

The assigned reader groups used in Lab 08 and the dynamic reader groups in Lab 15 are alternative membership paths to these same app roles. The code does not hard-code group names or query group membership.

## Windows PowerShell setup

From the root of a downloaded or cloned repository:

```powershell
Set-Location .\labs\08-enterprise-application-integration\app
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
notepad .env
```

Use Python 3.10 or later. Fill in `TENANT_ID`, `CLIENT_ID`, `CLIENT_SECRET`, `SESSION_SECRET`, and `REDIRECT_URI`. Generate a random session secret with:

```powershell
.\.venv\Scripts\python.exe -c "import secrets; print(secrets.token_hex(32))"
```

Copy that output privately into `SESSION_SECRET` in `.env`. Do not overwrite an existing configured `.env` when restarting the app.

Start the server:

```powershell
.\.venv\Scripts\python.exe app.py
```

Open **http://localhost:5000** on the same computer. Keep the terminal running during testing; press **Ctrl+C** to stop it. The app binds only to `127.0.0.1` and runs with debug disabled. Launching a My Apps tile is a separate portal behavior and is not required for these local tests.

## Routes and expected results

| Route | Behavior |
|---|---|
| `/` | Home and navigation |
| `/login` | Starts the MSAL authorization code flow |
| `/auth/callback` | Completes sign-in and stores selected identity claims |
| `/whoami` | Displays name, username, tenant/object identifiers, and roles |
| `/it` | Requires `IT.Reader`; returns 403 otherwise |
| `/procurement` | Requires `Procurement.Reader`; returns 403 otherwise |
| `/logout` | Clears the local session and redirects to Entra logout |

An unauthenticated protected-route request starts sign-in. A user with a valid app session but without the required role receives the application's **Forbidden** page. An unassigned user can instead be blocked by Entra with **AADSTS50105** before an application session is established.

## Troubleshooting

- **Requirements file not found:** run commands from this `app` directory.
- **Set SESSION_SECRET in .env before running:** check that the file is named `.env`, not `.env.txt`, and contains a random secret value.
- **Configure TENANT_ID, CLIENT_ID, CLIENT_SECRET:** complete the local configuration and restart Flask.
- **Redirect mismatch:** make the registered Web redirect match `REDIRECT_URI` exactly.
- **Old role still displayed:** close all test Incognito windows and sign in in a new one after confirming directory membership has changed.

## Scope and session behavior

This is a local teaching application, not a production deployment template. It uses MSAL's returned ID token claims for application sign-in and role checks. It does not implement the separate access-token validation API from Lab 12.

Flask's signed cookie session contains selected identity claims and the temporary sign-in flow state. Cookies are signed, not encrypted. The code does not store returned access or refresh tokens in the authenticated user session. It does not re-query Entra on each protected request or implement automatic session invalidation when assignments change. Removing a membership therefore does not prove termination of an existing application session.

The dependency file retains the restored package's version ranges; it is not a lockfile of the historical environment. Keep `.env`, client secrets, session secrets, cookies, and authentication responses out of screenshots and Git commits. Use fresh sessions to repeat the lab's access tests.

[Lab 08 results](../README.md) · [Lab 14](../../14-entitlement-management/README.md) · [Lab 15](../../15-dynamic-groups/README.md)
