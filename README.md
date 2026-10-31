# Microsoft Entra ID Administration & IAM Security Portfolio

This repository documents my hands-on Identity and Access Management (IAM) training in personal Microsoft Entra ID lab environments. It focuses on practical administration, identity lifecycle operations, access control, multifactor authentication, Conditional Access, Privileged Identity Management (PIM), SAML and OpenID Connect single sign-on, OAuth API authorization, and enterprise application troubleshooting.

Each lab records the scenario, configuration steps, observed outcomes, troubleshooting, and available screenshot evidence. These exercises are **personal lab experience**, not work performed in a production enterprise tenant.

## Featured Lab Results

| Area | Hands-on result |
|---|---|
| Privileged access | Validated eligible Helpdesk Administrator activation, approval, manual deactivation, automatic expiry, and password-reset denial outside active privilege windows |
| SAML federation | Configured SP-initiated SAML SSO, corrected a signing-certificate mismatch, and verified assignment removal blocks new sign-ins |
| OIDC troubleshooting | Captured PKCE authorization parameters, resolved consent and redirect failures, compared cache clearing with Entra logout, and verified denial after assignment removal |
| OAuth API authorization | Verified server token validation, 401 rejection of missing/tampered/ID tokens, 403 for insufficient scope, and 200 after write consent and a new token |
| Authentication recovery | Registered software OATH-TOTP, rejected incorrect and deleted-registration codes, and validated a replacement while preserving Authenticator push |
| Entitlement management | Verified self-service request, justified approval, one-hour application-role delivery, automatic expiry, and fresh-sign-in denial |
| Dynamic access | Verified Department-driven group and app-role changes, both transfer directions, and fresh-sign-in denial after automatic membership removal |
| Identity lifecycle | Tested joiner, mover, leaver, role changes, access reviews, and access removal with a fictional employee account |
| Conditional Access | Configured six policies; enabled four and retained two in Report-only mode |
| Administrator security | Registered and tested Windows Hello passkeys and verified an enforced phishing-resistant MFA requirement |
| Identity Protection | Evaluated Medium- and High-risk sign-in conditions using the What If simulator; no actual risky sign-in event was generated |
| Enterprise applications | Configured app roles, security group assignments, and assignment-required access for Gotham Access Lab |
| Authorization troubleshooting | Demonstrated an existing session retaining access after group removal, followed by a fresh sign-in denied with **AADSTS50105** |

## Lab Projects

| Lab | Project | Focus |
|---|---|---|
| 01 | [Employee Onboarding and Offboarding](labs/01-user-lifecycle/README.md) | User creation, attributes, group membership, sign-in, and offboarding |
| 02 | [Security Groups](labs/02-security-groups/README.md) | Group creation, assignment, and membership administration |
| 03 | [Administrative Roles](labs/03-admin-roles/README.md) | Entra directory roles and administrative permissions |
| 04 | [MFA Registration and Recovery](labs/04-mfa/README.md) | Microsoft Authenticator, security information, and authentication methods |
| 05 | [Sign-in Troubleshooting](labs/05-troubleshooting/README.md) | Diagnosing authentication failures through Entra sign-in logs |
| 06 | [Joiner–Mover–Leaver Identity Lifecycle](labs/06-joiner-mover-leaver/README.md) | Department transfer, group-based application access, access review, and offboarding |
| 07 | [Conditional Access and Identity Protection](labs/07-conditional-access/README.md) | MFA, phishing-resistant authentication, legacy-auth blocking policy, and risk simulations |
| 08 | [Enterprise Application Integration and Troubleshooting](labs/08-enterprise-application-integration/README.md) | OpenID Connect, app roles, My Apps visibility, consent, RBAC, and assignment-based access revocation |
| 09 | [Privileged Identity Management](labs/09-privileged-identity-management/README.md) | Eligible roles, MFA and justification requirements, approval-controlled activation, manual deactivation, automatic expiry, and audit correlation |
| 10 | [SAML 2.0 Single Sign-On](labs/10-saml-sso/README.md) | SAML endpoints, NameID, signing-certificate trust, SP-initiated SSO, and assignment-based access removal |
| 11 | [OpenID Connect SSO with PKCE](labs/11-oidc-sso/README.md) | Authorization Code with PKCE, claims, consent, redirect troubleshooting, cache/session behavior, and assignment removal |
| 12 | [OAuth 2.0 API Authorization](labs/12-oauth2-api-authorization/README.md) | Access-token validation, delegated scopes, admin consent, 401 versus 403, and read/write authorization |
| 13 | [Software OATH-TOTP Registration and Recovery](labs/13-oath-totp-recovery/README.md) | TOTP enrollment, incorrect-code rejection, registration deletion, and replacement-code validation |
| 14 | [Entitlement Management and Temporary Application Access](labs/14-entitlement-management/README.md) | Self-service requests, approval, app-role delivery, one-hour expiry, and access removal |
| 15 | [Dynamic Groups and Automated Department Transfers](labs/15-dynamic-groups/README.md) | Department rules, automatic membership, app-role changes, least privilege, and access removal |

## Lab Environments

The portfolio uses two intentional lab environments: **Labs 01–05** were completed in the original **Microsoft Entra ID Free** tenant (`phillipmcquinngmail.onmicrosoft.com`), while **Labs 06–15** were completed in the **Microsoft Entra ID P2** tenant (`GothamLabz.onmicrosoft.com`).

**Trial licensing:** I used a Microsoft Entra ID P2 free trial for Labs 06–15. On October 30, 2026, I verified an expiration date of **November 7, 2026** and disabled recurring renewal. The subscription was still Active. Post-expiry feature availability has not been tested.

### GothamLabz P2 environment

| Component | Lab configuration |
|---|---|
| Tenant domain | `GothamLabz.onmicrosoft.com` |
| License | Microsoft Entra ID P2 |
| Test identities | Fictional users and separate administrator accounts; Lab 09 added a dedicated PIM test account |
| Authentication | Microsoft Authenticator push, software OATH-TOTP, and device-bound Windows Hello passkeys |
| Access control | Assigned and department-based dynamic security groups, application roles, Conditional Access, and PIM eligible directory roles |
| Test applications | Gotham Access Lab — local Python Flask/OIDC application; Gotham SAML Lab — hosted SAML Toolkit integration; Gotham OIDC Lab — local MSAL SPA; Gotham OAuth API/Client Lab — local SPA and protected Python API |

For the environment snapshot through October 30, 2026, including historical Free-tenant context, P2 trial licensing, and evidence limits, see [Lab Setup](docs/lab-setup.md).

## IAM Skills Practiced

- **Identity lifecycle:** account creation, attribute updates, group management, joiner–mover–leaver processes, and offboarding.
- **Entitlement management:** catalogs, access packages, scoped self-service requests, justified approval, application-role delivery, and automatic assignment expiry.
- **Dynamic membership:** department-based rules, rule validation, automatic group changes, and application-role authorization after transfers.
- **Access control:** least privilege, role-based access control (RBAC), enterprise app assignments, and access reviews.
- **Privileged Identity Management:** time-limited eligibility, just-in-time role activation, justification, approval, manual deactivation, automatic expiry, and correlated audit events.
- **Authentication:** Microsoft Authenticator MFA, software OATH-TOTP registration and recovery, Windows Hello passkeys, and phishing-resistant authentication strengths.
- **Conditional Access:** policy targeting and exclusions, Report-only evaluation, staged enforcement, and sign-in investigation.
- **Identity Protection:** sign-in risk-based What If simulations using Entra ID P2.
- **Enterprise applications:** application roles, delegated Microsoft Graph permissions, administrator consent, OpenID Connect integration, SAML 2.0 federation and certificate trust, and sign-in failures such as `AADSTS50105`.
- **OAuth API authorization:** separate API/client registrations, exposed delegated scopes, RS256 token verification, audience/issuer/lifetime checks, least-privilege scope enforcement, and consent-based write enablement.
- **Troubleshooting and evidence:** Entra sign-in logs, audit investigation, session behavior, screenshots, and documented limitations.

## Evidence and Scope

Evidence is organized within each lab's `screenshots/` folder and linked from that lab's README. Results are explicitly differentiated:

- **Verified configuration:** a setting or assignment shown in the Entra portal.
- **Validated privileged operation:** password-reset success during active role windows, with denial before activation, while approval was pending, after deactivation, and after expiry.
- **MFA observation in Lab 09:** MFA was configured as an activation requirement, but no fresh MFA prompt was observed during the first activation; existing-claim satisfaction was not independently verified.
- **What If simulation:** a policy-matching test, not a real enforced authentication event.
- **Enforced sign-in:** an observed authentication event with an applicable Conditional Access result.
- **Observed without screenshot:** a result recorded during hands-on testing without a separate image.
- **Not tested:** a control without a corresponding real-world event, such as an actual legacy-client block or risky sign-in.

For the screenshot screening performed on October 30, 2026, see [Evidence Review](docs/evidence-review.md).

All employees, scenarios, and organization names in the labs are fictional. Secrets, passwords, authentication tokens, and local `.env` settings are not intended for publication.

## About This Portfolio

I built these labs to expand on my enterprise technical support experience and demonstrate practical skills relevant to IAM Analyst, Identity Security Analyst, Access Management Analyst, and Identity Operations roles.

[LinkedIn](https://www.linkedin.com/in/phillipmcquinn/)


