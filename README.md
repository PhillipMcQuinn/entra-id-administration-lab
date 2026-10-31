# Microsoft Entra ID Administration & IAM Security Portfolio

I built 17 hands-on labs covering identity administration, authentication, application access, and identity governance. I configured the environments and tested both permitted and denied access using separate administrator and fictional-user accounts. This is personal lab experience.

## Start Here

For a quick review, start with these three labs:

1. **[Lab 09 — Privileged Identity Management](labs/09-privileged-identity-management/README.md):** Temporary Helpdesk Administrator access, approval, automatic expiry, and password-reset denial outside active role windows.
2. **[Lab 12 — OAuth 2.0 API Authorization](labs/12-oauth2-api-authorization/README.md):** Runnable API and client, server-side token validation, and live 401, 403, and 200 results.
3. **[Lab 14 — Entitlement Management](labs/14-entitlement-management/README.md):** Self-service access requests, justified approval, one-hour app-role delivery, and fresh-sign-in denial after expiry.

Each includes configuration, screenshots, results, and a short **Limitations** section.

## Featured Lab Results

| Area | Demonstrated result |
|---|---|
| SSO troubleshooting | Corrected SAML certificate trust and OIDC redirect/consent failures — [Lab 10](labs/10-saml-sso/README.md) · [Lab 11](labs/11-oidc-sso/README.md) |
| Automated application access | Tested department-driven role changes and approval-controlled temporary group membership — [Lab 15](labs/15-dynamic-groups/README.md) · [Lab 16](labs/16-pim-for-groups/README.md) |
| Authentication and Conditional Access | Tested Authenticator recovery, administrator passkeys, and selected enforced MFA results — [Lab 04](labs/04-mfa/README.md) · [Lab 07](labs/07-conditional-access/README.md) · [Lab 13](labs/13-oath-totp-recovery/README.md) |
| Identity Protection | Verified administrator-generated High user risk and secured-password-change remediation through Graph — [Lab 17](labs/17-identity-protection/README.md) |

## Lab Projects

| Lab | Project | Focus |
|---|---|---|
| 01 | [Employee Onboarding and Offboarding](labs/01-user-lifecycle/README.md) | Onboarding and offboarding |
| 02 | [Security Groups](labs/02-security-groups/README.md) | Assigned membership and transfers |
| 03 | [Administrative Roles](labs/03-admin-roles/README.md) | Least privilege and role removal |
| 04 | [MFA Registration and Recovery](labs/04-mfa/README.md) | Authenticator enrollment and recovery |
| 05 | [Sign-in Troubleshooting](labs/05-troubleshooting/README.md) | Error diagnosis and recovery |
| 06 | [Joiner–Mover–Leaver Identity Lifecycle](labs/06-joiner-mover-leaver/README.md) | Lifecycle and application entitlements |
| 07 | [Conditional Access and Identity Protection](labs/07-conditional-access/README.md) | MFA, authentication strength, risk simulations |
| 08 | [Enterprise Application Integration and Troubleshooting](labs/08-enterprise-application-integration/README.md) | App roles, consent, session behavior |
| 09 | [Privileged Identity Management](labs/09-privileged-identity-management/README.md) | Eligibility, approval, activation, expiry |
| 10 | [SAML 2.0 Single Sign-On](labs/10-saml-sso/README.md) | Certificate trust and SSO recovery |
| 11 | [OpenID Connect SSO with PKCE](labs/11-oidc-sso/README.md) | PKCE, redirects, claims, sessions |
| 12 | [OAuth 2.0 API Authorization](labs/12-oauth2-api-authorization/README.md) | Token validation and delegated scopes |
| 13 | [Software OATH-TOTP Registration and Recovery](labs/13-oath-totp-recovery/README.md) | Registration deletion and replacement |
| 14 | [Entitlement Management and Temporary Application Access](labs/14-entitlement-management/README.md) | Requests, approval, delivery, expiry |
| 15 | [Dynamic Groups and Automated Department Transfers](labs/15-dynamic-groups/README.md) | Attribute-based membership and access |
| 16 | [PIM for Groups and Just-in-Time Application Access](labs/16-pim-for-groups/README.md) | Temporary membership and application access |
| 17 | [Identity Protection and Controlled User-Risk Remediation](labs/17-identity-protection/README.md) | Controlled user risk and remediation |

## Environment and Scope

I use **Gotham IAM Lab** as the fictional organization name. Labs **01–05** used Entra ID Free; Labs **06–17** used the separate GothamLabz Entra ID P2 trial tenant. The dated [environment setup](docs/lab-setup.md) records tenant separation, licensing, applications, recovery-account controls, and the final seven-policy inventory.

I operated all test identities myself, including requester and approver accounts. Individual labs distinguish configuration, What If simulations, observed behavior, and log-backed results. Their **Limitations** sections identify evidence gaps and untested controls.

## IAM Skills Practiced

Identity lifecycle · least privilege and RBAC · MFA and recovery · Conditional Access · PIM · entitlement management · dynamic groups · SAML/OIDC SSO · OAuth scopes and API token validation · sign-in and audit investigation.

## Evidence and Security

Screenshots are linked within each lab. The [October 31 security review](docs/evidence-review.md) documents screenshot screening, full-history secret scanning, false-positive triage, and confirmed GitHub Secret Protection and push-protection settings.

The personal Free-tenant domain is masked in current prose; historical screenshots and commits can still disclose it. Private `.env` files, passwords, secrets, and raw authentication tokens are excluded from the intended publication scope.

## License

My original application code and lab write-ups are available under the [MIT License](LICENSE), copyright 2026 Phillip McQuinn.

Third-party libraries retain their existing licenses and notices. Product UI screenshots, logos, and trademarks are excluded from this license grant and remain subject to their respective owners' rights.

## About Me

I built this portfolio to expand on my enterprise technical support experience and demonstrate practical skills for IAM Analyst, Identity Security Analyst, Access Management Analyst, and Identity Operations roles.

[LinkedIn](https://www.linkedin.com/in/phillipmcquinn/)
