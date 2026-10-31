# Microsoft Entra ID Lab Setup

> **Environment snapshot — October 31, 2026.** This file records my lab infrastructure and final documented configuration. Procedures, test results, cleanup evidence, and limitations belong in the individual [lab READMEs](../README.md#lab-projects).

## Purpose and Naming

I use **Gotham IAM Lab** as the fictional organization name throughout this portfolio. Earlier evidence contains the historical company attribute `Gotham IT Labs` and the tenant display label `Gotham Labs`; I preserve those labels when quoting actual saved values or portal text. They do not identify additional environments. Application names, group names, and tenant domains retain their configured values.

I operated the administrator and fictional test accounts myself in personal, nonproduction environments. Separate requester and approver accounts demonstrate an account-based workflow, not independent human approval.

## Tenant Environments

| Setting | Foundational environment | Advanced environment |
|---|---|---|
| Labs | 01–05 | 06–17 |
| Organization | Gotham IAM Lab | Gotham IAM Lab |
| Tenant domain | `<free-lab-tenant>.onmicrosoft.com` | `GothamLabz.onmicrosoft.com` |
| Edition used | Microsoft Entra ID Free | Microsoft Entra ID P2 free trial |
| Tenant type | Workforce | Workforce |

The Free-tenant domain shown here is a privacy placeholder. Historical screenshots and commits may still contain the original personal domain; see the [security review](evidence-review.md#privacy-and-history-limits).

These are two intentional tenant environments, not a domain rename or migration. P2 describes the advanced lab environment; it does not mean every feature demonstrated there requires P2.

## Accounts and Administration

| Account or group of identities | Environment role |
|---|---|
| Regular administrator | Tenant and application configuration; direct, permanently active Global Administrator in the P2 snapshot |
| Lab Recovery Administrator | Separate P2 recovery account; direct, permanently active Global Administrator; excluded from the enforced policy scopes documented in Lab 07 |
| Fictional employees | Bruce Wayne, Alfred Pennyworth, Lucius Fox, Barbara Gordon, Dick Grayson, Selina Kyle, and Tim Drake across the lab scenarios |
| PIM Test Administrator | Dedicated P2 directory-role test account introduced in Lab 09 |

Account creation, deletion, membership, and temporary role assignments vary by lab. This table describes account purposes, not a current directory inventory. The October 31 PIM active-assignment screenshot again showed the regular and recovery accounts as direct, permanent Global Administrators; lab-specific cleanup is documented with each exercise.

**PIM test-account retirement — October 31, 2026:** After completing repeat testing, I checked the PIM assignment lists: the active list showed only my regular and recovery Global Administrators, and the eligible list returned no results for Pim-Test. I removed the directly assigned Entra ID P2 license in Microsoft 365 Admin Center, verified Licenses (0), and deleted PIM Test Administrator. The portal confirmed deletion; I did not permanently purge the deleted account. The license page showed 16 of 25 P2 licenses available after removal.

## Groups and Application Roles

| Group | Membership or purpose |
|---|---|
| `SG-IT-Employees`, `SG-Executive-Employees`, `SG-Procurement-Employees` | Assigned department groups in the foundational tenant |
| `SG-Lab-Test-Users` | Assigned test-user group in the foundational tenant |
| `SG-GothamApp-IT-Readers` | Assigned group mapped to `IT.Reader` |
| `SG-GothamApp-Procurement-Readers` | Assigned group mapped to `Procurement.Reader` |
| `DG-GothamApp-IT-Readers` | Dynamic Department IT group mapped to `IT.Reader`; introduced in Lab 15 |
| `DG-GothamApp-Procurement-Readers` | Dynamic Department Procurement group mapped to `Procurement.Reader`; introduced in Lab 15 |
| `PIM-GothamApp-Procurement-Readers` | PIM-managed group mapped to `Procurement.Reader`; introduced in Lab 16 |
| `SG-CA-Lab-Users` | Regular-user Conditional Access scope |
| `SG-Auth-WindowsHello-Admins` | Regular administrator passkey configuration scope |
| `SG-Auth-WindowsHello-Recovery` | Recovery administrator passkey configuration scope |

Application permissions depend on configured group-to-role assignments, not group names alone. Current membership and eligibility are described in the relevant lab's final-state section.

## Authentication and Conditional Access

The documented authentication methods include Microsoft Authenticator push, software OATH-TOTP, and device-bound Windows Hello passkeys. I did not use a FIDO2 hardware security key. The Free-tenant MFA exercise used Security Defaults; **Security Defaults remained disabled in the P2 environment** after the Lab 07 transition to Conditional Access.

**Recovery-account controls and limits:** I verified a Windows Hello passkey sign-in and administrative access for the separate recovery account, with a permanently active Global Administrator assignment. On October 31, I confirmed that my passwords are stored on an encrypted storage device that I disconnect and store separately when it is not in use. Encrypted offline storage and physical separation are operator-confirmed; a recovery test using the stored credentials was not recorded. Automated alerts on every recovery-account sign-in have not been configured or tested. On October 31, the Diagnostic settings page reported that an Azure subscription was required. I did not create a subscription, configure a Log Analytics destination, or test Azure Monitor alert delivery; that alerting path remains blocked pending an available subscription. This observation does not establish that all other possible notification mechanisms are unavailable. They remain hardening items; I do not claim that the policy exclusion is fully compensated by monitoring or that this single recovery account implements Microsoft's complete emergency-access design. See [Lab 07](../labs/07-conditional-access/README.md#recovery-account-controls-and-remaining-hardening) and [Microsoft's emergency-access guidance](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/security-emergency-access).

### Policy inventory after Lab 17

| Policy | Final documented state | Purpose | Introduced |
|---|---|---|---|
| `CA-00-Lab-Admin-MFA` | On | Regular administrator MFA | Lab 07 |
| `CA-01-Lab-Users-MFA` | On | Scoped regular-user MFA | Lab 07 |
| `CA-02-Admins-PhishingResistant` | On | Administrator phishing-resistant authentication strength | Lab 07 |
| `CA-03-Lab-Block-Legacy` | On | Scoped legacy-client block | Lab 07 |
| `CA-04-Lab-Recovery-MFA` | Report-only | Recovery-account authentication evaluation | Lab 07 |
| `CA-05-Lab-SignInRisk-MFA` | Report-only | Medium/High sign-in-risk evaluation | Lab 07 |
| `CA-06-Lab-Tim-High-User-Risk-Remediation` | Report-only | Tim-only High user-risk remediation | Lab 17 |

**Timeline:** Lab 07 ended with six policies: four On and two Report-only. I added CA-06 in [Lab 17](../labs/17-identity-protection/README.md) and returned it to Report-only after testing. The October 31 snapshot therefore contains **seven policies: four On and three Report-only**. The earlier six-policy inventory is historical, not a different count of the final configuration.

I rechecked the full policy list on October 31 after retiring Pim-Test. It showed seven user-created policies, zero Microsoft-managed policies, and the states listed above: four On and three Report-only.

Policy state records configuration, not proof of every intended enforcement outcome. Targeting, exclusions, simulations, actual sign-in results, and evidence limits remain in [Lab 07](../labs/07-conditional-access/README.md) and [Lab 17](../labs/17-identity-protection/README.md).

## Applications and Local Tools

| Application | Platform and local setup | Configuration and results |
|---|---|---|
| Gotham Access Lab | Python Flask/OIDC; `http://localhost:5000`; Web redirect `http://localhost:5000/auth/callback`; app roles `IT.Reader` and `Procurement.Reader`; assignment required | [Lab 08](../labs/08-enterprise-application-integration/README.md) · [App source and setup](../labs/08-enterprise-application-integration/app/README.md) |
| Gotham SAML Lab | Microsoft Entra SAML Toolkit gallery integration | [Lab 10](../labs/10-saml-sso/README.md) |
| Gotham OIDC Lab | Local MSAL browser SPA at `http://localhost:3000`; Authorization Code with PKCE | [Lab 11](../labs/11-oidc-sso/README.md) · [App setup](../labs/11-oidc-sso/app/README.md) |
| Gotham OAuth API and Client Lab | Local browser SPA and protected Python API; delegated `Inventory.Read` and `Inventory.Write` scopes | [Lab 12](../labs/12-oauth2-api-authorization/README.md) · [App setup](../labs/12-oauth2-api-authorization/app/README.md) |

I used a Windows workstation, separate browser sessions for account testing, Microsoft Entra admin center, Microsoft Authenticator, Windows Hello, and Graph Explorer. Exact application identifiers, redirect configurations, dependencies, and runnable instructions remain with the applicable application lab.

## Licensing Snapshot and Planned Transition

On **October 30, 2026**, I verified that the P2 free trial was Active with **10 of 25 licenses assigned**, an expiration date of **November 7, 2026**, and recurring renewal disabled. A separate billing field showed November 8; I used November 7 as the preparation deadline. This is a dated observation, not a live licensing query.

I exported the six policies present on October 30. On October 31, I also downloaded the CA-06 JSON export and reconfirmed its Report-only state. The download was operator-confirmed; the exported file's contents were not inspected in this review. Policy exports remain outside this public repository.

After removing Pim-Test's direct P2 assignment on October 31, its page showed Licenses (0) and 16 of 25 P2 licenses available (9 assigned). This later count supersedes the October 30 assigned-seat count without changing the trial expiry/renewal observation.

The planned return to Security Defaults and later post-expiry observations have not been completed. I will document those changes separately rather than infer them from the trial end date.

## Where to Find Procedures and Results

The [portfolio lab index](../README.md#lab-projects) links all 17 exercises. Detailed results are maintained once, in their lab READMEs:

| Area | Detailed documentation |
|---|---|
| Foundational users, groups, roles, MFA, and troubleshooting | Labs 01–05 in the [lab index](../README.md#lab-projects) |
| Lifecycle, Conditional Access, and enterprise applications | [Lab 06](../labs/06-joiner-mover-leaver/README.md) · [Lab 07](../labs/07-conditional-access/README.md) · [Lab 08](../labs/08-enterprise-application-integration/README.md) |
| Directory-role PIM | [Lab 09](../labs/09-privileged-identity-management/README.md) |
| SAML, OIDC, and OAuth | [Lab 10](../labs/10-saml-sso/README.md) · [Lab 11](../labs/11-oidc-sso/README.md) · [Lab 12](../labs/12-oauth2-api-authorization/README.md) |
| Software OATH-TOTP recovery | [Lab 13](../labs/13-oath-totp-recovery/README.md) |
| Entitlement management | [Lab 14](../labs/14-entitlement-management/README.md) |
| Dynamic groups | [Lab 15](../labs/15-dynamic-groups/README.md) |
| PIM for Groups | [Lab 16](../labs/16-pim-for-groups/README.md) |
| Identity Protection user-risk remediation | [Lab 17](../labs/17-identity-protection/README.md) |

## Evidence and Maintenance

I keep screenshots, test outcomes, cleanup, and unverified items in the relevant lab. Configuration, What If simulations, observed prompts, and enforced sign-in results are distinct evidence types. The dated [evidence review](evidence-review.md) describes its own screening scope.

I keep passwords, authentication QR codes, recovery codes, tokens, private keys, application secrets, cookies, and actual `.env` files out of the public repository. Published `.env.example` files contain placeholders.

When the environment changes, I update the snapshot date, policy inventory, and infrastructure facts here, while retaining historical test results in their original lab context.

[Return to portfolio](../README.md)
