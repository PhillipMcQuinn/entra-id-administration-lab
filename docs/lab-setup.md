# Microsoft Entra ID Lab Setup

> **Environment snapshot — October 31, 2026:** Labs 01–05 use the original Entra ID Free tenant. Labs 06–17 use the separate GothamLabz tenant with a **P2 free trial**. The October 5 setup values are retained below as historical context; the GothamLabz column and later lab sections record the subsequent environment. I verified the trial expiration date as November 7, 2026 and disabled recurring renewal. Post-expiry feature availability has not been tested.

## Purpose and Scope

This document describes the configuration used for personal, hands-on Microsoft Entra ID and Identity and Access Management (IAM) training. Employee identities, departments, and application resources are fictional. Tests were conducted in nonproduction lab environments. Screenshots and results for individual controls are maintained in their respective lab READMEs.

## Lab Environment Overview

This portfolio uses two separate Microsoft Entra ID environments to demonstrate progression from foundational identity administration to advanced Identity and Access Management (IAM) security controls.

### Environment 1 — Microsoft Entra ID Free (Labs 01–05)

**Tenant:** `phillipmcquinngmail.onmicrosoft.com`  
**License:** Microsoft Entra ID Free

This environment was used for introductory IAM administration exercises:

- Lab 01: User Lifecycle Management
- Lab 02: Security Group Administration
- Lab 03: Administrative Roles and Permissions
- Lab 04: MFA Registration and Recovery
- Lab 05: Sign-in Troubleshooting

### Environment 2 — Microsoft Entra ID P2 (Labs 06–17)

**Tenant:** `GothamLabz.onmicrosoft.com`  
**License:** Microsoft Entra ID P2 free trial

This environment was used for advanced IAM security, governance, and application-integration exercises. P2 describes the environment; SAML, OIDC, and OAuth API authorization are not presented as P2-only features:

- Lab 06: Joiner–Mover–Leaver Identity Lifecycle Management
- Lab 07: Conditional Access and Identity Protection
- Lab 08: Enterprise Application Integration and Troubleshooting
- Lab 09: Privileged Identity Management
- Lab 10: SAML 2.0 Single Sign-On
- Lab 11: OpenID Connect SSO with Authorization Code and PKCE
- Lab 12: OAuth 2.0 API Authorization with Delegated Scopes
- Lab 13: Software OATH-TOTP Registration and Recovery
- Lab 14: Entitlement Management and Temporary Application Access
- Lab 15: Dynamic Groups and Automated Department Transfers
- Lab 16: PIM for Groups and Just-in-Time Application Access
- Lab 17: Identity Protection and Controlled User-Risk Remediation

Labs 06–08 recorded two administrator accounts and seven standard user accounts, Microsoft Authenticator enrollment, Windows Hello passkeys for administrators, Conditional Access policies, and group-based application role assignments. Lab 09 added a dedicated PIM test account with an Entra ID P2 license and Microsoft Authenticator registration. Its eligible Helpdesk Administrator assignment was removed during cleanup.

### Environment Separation

Configuration settings, licenses, user accounts, and test results should be interpreted within their respective environments rather than assumed to apply across both tenants.

| Setting | Original setup record (October 5, 2026) | GothamLabz lab configuration (October 8–31, 2026) |
|---|---|---|
| Organization label | Gotham IAM Lab | Gotham IAM Lab / Gotham IT Labs; Gotham Labs in Lab 09 |
| Tenant type | Workforce | Microsoft Entra workforce identity lab |
| Recorded tenant domain | `phillipmcquinngmail.onmicrosoft.com` | `GothamLabz.onmicrosoft.com` |
| Licensing | Microsoft Entra ID Free | Microsoft Entra ID P2 assigned for lab accounts |
| Operating system | Windows 11 | Windows workstation used for the local application exercises |
| Browser | DuckDuckGo recorded at setup | Browser sessions used for administration, sign-in, and Windows Hello tests; exact browser varies by test |
| Authenticator | Microsoft Authenticator | Microsoft Authenticator; Windows Hello passkeys on administrator accounts |
| Admin center | [Microsoft Entra admin center](https://entra.microsoft.com) | [Microsoft Entra admin center](https://entra.microsoft.com) |

The two tenant domains represent separate environments, not a domain rename or migration. Labs 01–05 retain their original Free-tenant context; Labs 06–17 use GothamLabz.

## Administrator and Test Accounts

### Administrator accounts

The later GothamLabz exercises used two distinct administrator accounts: a regular Global Administrator and a recovery administrator. Both were tested with Windows Hello passkeys and Microsoft Authenticator. The recovery administrator was excluded from the enforced Conditional Access policy scope to reduce lockout risk. The original setup recorded a single named Global Administrator; it did not document the recovery administrator at that time.

| Account / account type | Role or use | Verified lab purpose |
|---|---|---|
| Regular administrator | Global Administrator | Configure and test tenant, enterprise application, and security controls |
| Recovery administrator | Separate administrator account | Recovery access and verification of Conditional Access exclusions |

Labs 06–08 recorded **nine accounts: two administrators and seven standard test users**, with P2 license assignments and MFA registration checked during those exercises. Lab 09 added **PIM Test Administrator** (`Pim-Test@GothamLabz.onmicrosoft.com`) as a dedicated, separately licensed test identity. This historical count is not a current tenant inventory. Do not infer the number of purchased licenses from assigned accounts.

### Fictional test users

Original lab documentation included the following fictional employees:

| Display name | Username prefix | Job title | Department | Manager |
|---|---|---|---|---|
| Bruce Wayne | `BruceWayne` | Chief Executive Officer | Executive | Phillip McQuinn |
| Alfred Pennyworth | `AlfredPennyworth` | Assistant Executive | Executive | Bruce Wayne |
| Lucius Fox | `LuciusFox` | IT Director | IT | Bruce Wayne |
| Barbara Gordon | `BarbaraGordon` | Systems Administrator | IT | Lucius Fox |
| Dick Grayson | `DickGrayson` | Support Specialist | IT | Lucius Fox |
| Selina Kyle | `SelinaKyle` | Procurement Specialist | Procurement | Bruce Wayne |

Later labs also used **Tim Drake** (`TimDrake@GothamLabz.onmicrosoft.com`) for Joiner–Mover–Leaver and enterprise application access testing. His department changed from IT to Procurement during the lifecycle exercise. For the final Lab 08 state, his account remained enabled but his membership in `SG-GothamApp-Procurement-Readers` was removed.

Usernames in each tenant use that tenant's actual `.onmicrosoft.com` domain. Employee identifiers and dates in the exercises are fictional and should not be interpreted as production HR records.

## Groups, Application Roles, and Access Assignments

### General-purpose groups recorded in the original setup

| Group | Membership type | Training purpose |
|---|---|---|
| `SG-IT-Employees` | Assigned | IT department membership |
| `SG-Executive-Employees` | Assigned | Executive department membership |
| `SG-Lab-Test-Users` | Assigned | Test-user organization |
| `SG-Procurement-Employees` | Assigned | Procurement department membership |

### Additional groups used in the later labs

| Group | Training purpose |
|---|---|
| `SG-GothamApp-IT-Readers` | Assign `IT.Reader` access in Gotham Access Lab |
| `SG-GothamApp-Procurement-Readers` | Assign `Procurement.Reader` access in Gotham Access Lab |
| `DG-GothamApp-IT-Readers` | Dynamic Department IT membership; assigned IT.Reader in Lab 15 |
| `DG-GothamApp-Procurement-Readers` | Dynamic Department Procurement membership; assigned Procurement.Reader in Lab 15 |
| `SG-CA-Lab-Users` | Scope lab-user Conditional Access testing |
| `Managers` | Group referenced in an earlier Conditional Access manager/device-control exercise |

Group membership **does not automatically grant permissions to arbitrary applications**. The Gotham Access Lab enterprise application was configured with group-to-application-role assignments, which linked the reader groups to `IT.Reader` and `Procurement.Reader` respectively. The application required users to be assigned. Individual lab READMEs record the membership and access tests.

## Authentication and Security Configuration

### Authentication methods

- Microsoft Authenticator registration was checked for the GothamLabz accounts.
- Lab 13 added a separate software OATH-TOTP method for Selina Kyle, tested deletion and replacement, and retained her existing Authenticator push registration.
- Windows Hello passkeys were registered and tested for the regular and recovery administrator accounts.
- No FIDO2 hardware security key was used in the documented exercises.
- The passkey results demonstrate the tested administrator authentication flows; they should not be read as proof that all users or all sign-ins used phishing-resistant authentication.

### Security Defaults and Conditional Access

**Security Defaults were disabled** to permit targeted Conditional Access policy configuration and testing. The following policy inventory was recorded during Lab 07:

| Policy | Recorded state | Purpose or verification |
|---|---|---|
| `CA-00-Lab-Admin-MFA` | On | Administrative MFA |
| `CA-01-Lab-Users-MFA` | On | MFA for scoped lab users; successful user sign-in documented |
| `CA-02-Admins-PhishingResistant` | On | Phishing-resistant authentication strength for administrators; successful administrative sign-in recorded |
| `CA-03-Lab-Block-Legacy` | On | Block legacy authentication; evaluated using What If, **not** a real legacy-auth attempt |
| `CA-04-Lab-Recovery-MFA` | Report-only | Recovery-account related policy evaluation |
| `CA-05-Lab-SignInRisk-MFA` | Report-only | Sign-in risk scenarios assessed using What If, **not** a generated real risky sign-in |

The recovery administrator was excluded from enforced policies in the documented configuration. Four policies were **On** and two were **Report-only** at the time of Lab 07 testing. A report-only result or What If calculation is not the same as an enforced sign-in result. Consult [Lab 07](../labs/07-conditional-access/README.md) for individual evidence.

## Enterprise Application Integration

**Gotham Access Lab** is a locally hosted Python Flask application used to test Microsoft Entra sign-in, application-role claims, group-based authorization, assignment requirements, and access revocation.

| Setting | Configuration or observed result |
|---|---|
| Application | Gotham Access Lab |
| Application (client) ID | `5f817a6e-cecc-4819-ae39-e28b2b02f25e` |
| Local app URL | `http://localhost:5000` |
| Redirect URI | `http://localhost:5000/auth/callback` |
| Application roles | `IT.Reader`, `Procurement.Reader` |
| Assignment required | Yes |
| Visible to users | Changed from No to Yes during troubleshooting |
| Microsoft Graph delegated permission | `User.Read`; admin consent shown as granted when reviewed |

In Lab 08, Tim Drake was allowed into the Procurement resource and denied access to IT Inventory while he had the Procurement Reader role. After his Procurement Readers group membership was removed, the existing Flask session continued permitting access. A fresh sign-in failed with **AADSTS50105** because he no longer had an application assignment. The Entra sign-in log showed failure code **50105**. This is an **application assignment** failure, not proof of Conditional Access enforcement or account disablement.

The My Apps tile became visible after changing the visibility property, but the tile launch initially failed. Successful authentication was subsequently demonstrated with the locally running Flask application; the original My Apps tile-launch issue was **not independently verified as resolved**.

See [Lab 08](../labs/08-enterprise-application-integration/README.md) for the detailed procedure, observations, and evidence.

## Privileged Identity Management (Lab 09)

Lab 09 used Microsoft Entra PIM for **directory roles**, with a dedicated test identity and separate requester and approver browser sessions.

| Setting | Lab configuration |
|---|---|
| Test account | PIM Test Administrator (`Pim-Test@GothamLabz.onmicrosoft.com`) |
| License and authentication | Entra ID P2 assigned; Microsoft Authenticator registered |
| Role and scope | Helpdesk Administrator; Directory / Gotham Labs |
| Assignment | Direct, eligible, time-limited; originally scheduled October 29–30, 2026 |
| Maximum activation duration | 1 hour |
| Activation requirements | Azure MFA and justification |
| Approval | Off for the first activation; enabled for the second activation |
| Approver | Main Global Administrator account, Phillip McQuinn |
| Permission test | Password reset for fictional user Dick Grayson |
| Audit evidence | Activation, manual deactivation, approval, and automatic expiry; second activation events correlated by ID |

Password resets were blocked before activation, succeeded while the role was active, and were blocked after manual deactivation. The second request remained pending approval with password resets blocked; after approval and activation, the reset succeeded. The approved activation was left to expire automatically, and a subsequent reset was denied.

**MFA evidence limitation:** MFA was configured as an activation requirement, but no fresh MFA prompt was observed during the first activation. Whether an existing MFA claim satisfied the requirement was not independently verified. Authenticator registration alone does not establish an MFA challenge at activation.

The requester and approver were separate accounts operated by the lab owner. This demonstrates account separation and an approval workflow, not independent human review.

### Final Lab 09 state

- The eligible Helpdesk Administrator assignment was removed during cleanup.
- No active administrator roles or pending requests remained for Pim-Test.
- Dick Grayson signed in using the latest temporary password and completed the password change.
- Deletion of the Pim-Test account was not reported.
- The final Helpdesk Administrator role settings required MFA, justification, and approval with a 1-hour maximum. Restoration of the earlier settings was not reported.

See [Lab 09](../labs/09-privileged-identity-management/README.md) for the complete findings and screenshot evidence. Audit timestamps reproduce the portal's displayed values; a timezone label was not captured.

## Tools and Local Workstation

- Microsoft Entra admin center: users, groups, application registrations, enterprise applications, authentication, licensing, Conditional Access, and Privileged Identity Management.
- Microsoft Authenticator: MFA registration and authentication.
- Windows Hello: administrator passkey registration and testing.
- Python and Flask: local Gotham Access Lab application used for sign-in and authorization tests.
- Sign-in logs, audit logs, Conditional Access What If, and access review interfaces: investigation and verification.
- GitHub: lab narratives and selected screenshot evidence.

The local Flask app uses a private `.env` file for sensitive configuration. Commit only a redacted `.env.example`; **never commit a client secret, session secret, token, or real `.env`**.

## Verification Summary

| Check | Observed outcome | Documentation |
|---|---|---|
| Fictional user and group administration | User attributes and group membership inspected | Labs 01–03 and 06 |
| Test-user authentication | Successful sign-ins and selected failures investigated | Labs 04–05 |
| Joiner–Mover–Leaver | Reader permissions changed and denied on removal; offboarding tests recorded | [Lab 06](../labs/06-joiner-mover-leaver/README.md) |
| Entra ID P2 and MFA | Licensing and MFA registration checked for GothamLabz test accounts | [Lab 07](../labs/07-conditional-access/README.md) |
| Conditional Access | Four policies On, two Report-only; selected successful sign-in logs reviewed | [Lab 07](../labs/07-conditional-access/README.md) |
| Enterprise application RBAC | Procurement Allowed; IT Inventory Denied for Procurement Reader | [Lab 08](../labs/08-enterprise-application-integration/README.md) |
| Assignment revocation | Fresh sign-in denied with AADSTS50105; existing-session access persisted until sign-out | [Lab 08](../labs/08-enterprise-application-integration/README.md) |
| PIM activation and revocation | Password reset succeeded only while the role was active; denied before activation, after manual deactivation, and after automatic expiry | [Lab 09](../labs/09-privileged-identity-management/README.md) |
| PIM approval and audit | Pending request did not grant password-reset access; approval, activation, and expiry audit evidence captured | [Lab 09](../labs/09-privileged-identity-management/README.md) |

## Evidence and Security Handling

- Screenshots use fictional employees and training resources.
- Descriptions distinguish **configured**, **What If / Report-only**, **observed**, and **enforced/tested** results.
- Screenshots may not prove every configuration action completed; the relevant lab notes any evidence limitations.
- Passwords, recovery codes, authentication QR codes, access/refresh tokens, private keys, application secrets, and session cookies must not be published.
- Review screenshots for personal account information and sensitive browser content before uploading.

## SAML 2.0 Single Sign-On (Lab 10)

**Gotham SAML Lab** uses the Microsoft Entra SAML Toolkit gallery integration and Dick Grayson as the fictional test user.

| Setting | Final configuration |
|---|---|
| Application ID | `6cc23aab-ec11-40bb-a9ae-9a5a1c9be07d` |
| Flow tested | SP-initiated SAML SSO |
| Entity ID | `https://samltoolkit.azurewebsites.net` |
| Reply URL / ACS | `https://samltoolkit.azurewebsites.net/SAML/Consume/22845` |
| Sign on URL | `https://samltoolkit.azurewebsites.net/SAML/Login/22845` |
| NameID | Email address format; `user.userprincipalname` |
| Signing | Sign SAML assertion; SHA-256 |
| Active application certificate expiry | October 29, 2029 |
| Assignment required | Yes |
| Final users and groups | No assignments |

The first toolkit connection trusted a different certificate, and the service provider returned a processing error. Its edit page also failed, so a replacement connection was created with the downloaded application Certificate (Raw), and Entra endpoints were updated to match. SSO then succeeded on the toolkit and in the matching Entra sign-in log. The log recorded MFA satisfied by an existing token claim.

Unassigned access was denied with AADSTS50105. After successful assigned-user testing, Dick's assignment was removed and a fresh sign-in was denied again. Existing application-session termination and SAML logout were not tested. Deletion of the original toolkit connection and local toolkit accounts was not confirmed.

See [Lab 10](../labs/10-saml-sso/README.md) for configuration, certificate troubleshooting, validation, and evidence.

## OpenID Connect SSO with PKCE (Lab 11)

Gotham OIDC Lab is a single-tenant browser SPA using MSAL Browser 5.27.0, served at `http://localhost:3000/lab.html` with a dedicated root redirect bridge at `http://localhost:3000/`. Client ID: `0ab52627-9b78-4bb9-b721-82916d824e69`. No client secret was used. Implicit grants remained unchecked and public client flows disabled. Admin consent was granted for delegated `openid`, `profile`, and `offline_access`.

Captured authorization parameters included `response_type=code`, `code_challenge`, and `code_challenge_method=S256`. Five teaching claim comparisons passed; they are not independent signature validation. Assignment and consent failures were resolved, a deliberate AADSTS50011 redirect mismatch was recovered, and an app logout cleanup issue was corrected.

Clearing the app cache allowed sign-in without new password/MFA prompts. After corrected Entra logout, I observed password and MFA prompts. The matching 20:19:32 UTC success log records MFA as previously satisfied; it does not independently prove a fresh challenge. App/log correlation ID: `01a18950-cc3f-71a4-9332-b70c8e9009ce`.

Final state: Dick's assignment removed; new sign-in denied with AADSTS50105 after app-cache clearing; Phillip's assignment retained; Assignment required Yes; Visible to users No. Existing-token revocation was not tested. Registration and consent retained; I stopped the local server.

See [Lab 11](../labs/11-oidc-sso/README.md) for results, source, and evidence.

## OAuth 2.0 API Authorization (Lab 12)

Created separate single-tenant registrations for **Gotham OAuth API Lab** (API client ID `487fb7d7-495e-4291-bf03-e0eba9367167`) and **Gotham OAuth Client Lab** (SPA client ID `529b206d-0fd4-4d9e-a31e-19a9e6177158`). The API exposes admins-only delegated `Inventory.Read` and `Inventory.Write` scopes under `api://487fb7d7-495e-4291-bf03-e0eba9367167`, with requestedAccessTokenVersion set to 2. The client uses the SPA redirect `http://localhost:3000/`, implicit grants off, public client flows disabled, and no client secret.

A local MSAL Browser 5.27.0 SPA and Python API run on the same loopback origin. The API uses PyJWT 2.15.1 and cryptography 50.0.2 to verify RS256 signatures with Entra public keys, issuer, API audience, lifetime, tenant, version, allowed client, and delegated scopes. The API is a teaching implementation using Python's development HTTP server.

Dick Grayson acquired Inventory.Read. Live tests returned read **200**, missing-token **401**, tampered-signature **401**, client-ID-token **401**, and read-only write **403** with token validation passed and insufficient_scope. After Inventory.Write was added and admin consent granted, a newly acquired token contained both scopes and the write returned **200**, increasing the fictional quantity from 10 to 11. Six results were captured together in the test history. API request IDs are local identifiers, not Entra correlation IDs.

I signed out through Entra and stopped the server. Both registrations and consent were retained. No Lab 12 Entra sign-in-log correlation, fresh-MFA proof, raw protocol capture, or live expired-token test was collected. Twenty offline regression tests used disposable fixture keys; they are separate from the six live results.

See [Lab 12](../labs/12-oauth2-api-authorization/README.md) for evidence, limitations, and runnable source.

## Software OATH-TOTP Registration and Recovery (Lab 13)

I inspected the Software OATH policy: enabled for All users, Registration Optional. I left that policy unchanged. Using Selina Kyle's fictional account, I registered a separate TOTP entry in Microsoft Authenticator while preserving the existing push registration on Pixel 10 Pro XL.

I successfully signed in with a valid code, captured rejection of an incorrect code, and successfully retried with the correct code. I then deleted only the Software OATH registration as administrator and captured rejection of a code from the old phone entry. I registered a replacement and successfully logged in with its new code. The final Security info screenshot shows TOTP and push registrations together.

The captured successful sign-in logs recorded MFA satisfied by an existing token claim / Previously satisfied. They do not independently prove a fresh OATH challenge; code-based success is my observed test result. Both methods were on one phone, so this was not a full lost-device recovery exercise. Old phone-entry deletion and final sign-out were recommended but not confirmed.

See [Lab 13](../labs/13-oath-totp-recovery/README.md) for the test matrix, evidence, final state, and limitations.

## Entitlement Management (Lab 14)

I created the internal-only **Gotham Application Access** catalog and added Gotham Access Lab as an application resource. I created **Gotham Procurement Reader - Temporary Access**, scoped requests to Tim Drake, required requestor and approver justification, selected my administrator account as approver, and configured one-hour assignment expiry with no extensions.

I operated both accounts myself in separate browser sessions. Tim remained blocked with AADSTS50105 before approval and while pending. After approval, the package delivered a direct application assignment and his token displayed only Procurement.Reader. Procurement access succeeded and IT Inventory was forbidden. The assignment expired at its configured end time of October 30, 2026, 2:28:50 PM MDT; I observed roughly four minutes before Expired appeared. I confirmed automatic removal of Tim's direct application assignment and denial of a fresh sign-in. I stopped Flask after testing. Existing-session termination was not tested.

See [Lab 14](../labs/14-entitlement-management/README.md) for configuration, results, screenshots, and evidence limits.

## Dynamic Groups and Department Transfers (Lab 15)

I created separate dynamic security groups for Department IT and Procurement and assigned them to the corresponding Gotham Access Lab roles. I validated Tim against both rules, waited for initial processing, and verified the actual Procurement membership and application baseline.

I changed Department from Procurement to IT at 5:12 PM MDT, back to Procurement at 5:17 PM, and to Lab-NoAccess at 5:21 PM on October 30. I observed each membership change within one minute. Fresh application sessions displayed only the matching department role, allowed its protected page, and denied the other department page. With neither reader membership, a fresh sign-in failed with AADSTS50105. The initial group population was slower; its exact completion time was not measured.

I restored Department Procurement and confirmed its dynamic membership returned within one minute. Tim's final groups were DG-GothamApp-Procurement-Readers and SG-CA-Lab-Users. I retained both dynamic group-to-role assignments and the original assigned groups. I stopped Flask and closed test Incognito windows. I did not test automatic termination of existing application sessions.

See [Lab 15](../labs/15-dynamic-groups/README.md) for rules, role-assignment audit properties, test results, timing limits, and screenshots.

## PIM for Groups (Lab 16)

I created the assigned cloud security group **PIM-GothamApp-Procurement-Readers** (`642c23fd-62ee-4196-a2f0-01700833fe6b`), managed it through PIM, and assigned it Procurement Reader in Gotham Access Lab. Member activation required Azure MFA, justification, approval by my administrator account, and a maximum duration of one hour. I gave Tim a one-day eligible Member assignment and temporarily changed Department to Lab-NoAccess at 8:06 PM MDT on October 30. His dynamic reader membership disappeared within one minute.

Fresh application sign-in failed with AADSTS50105 before activation and while approval was pending. I operated requester and approver accounts myself. No fresh MFA prompt was observed during the request; existing-claim satisfaction was not independently verified. After approval, Tim's activated membership ran from 8:18:54 PM to 9:18:53 PM MDT. A fresh session displayed Procurement.Reader only, allowed Procurement, and denied IT Inventory.

After automatic expiry, the PIM group was already absent when I loaded Tim's Groups page, PIM no longer listed him as active, and a fresh sign-in failed with AADSTS50105. I did not measure exact removal latency or test existing-session termination. I removed his remaining eligibility, restored Department Procurement and its dynamic membership, stopped Flask, and closed test Incognito windows. I retained the PIM group, settings, application assignment, and my permanent Owner assignment.

See [Lab 16](../labs/16-pim-for-groups/README.md) for configuration, the validation matrix, screenshots, and evidence limits.

## Identity Protection and User-Risk Remediation (Lab 17)

On October 31, I created **CA-06-Lab-Tim-High-User-Risk-Remediation**, scoped to Tim Drake only, All resources, and High user risk. Its saved requirements were risk remediation, Multifactor authentication strength, and a new sign-in for each session. I compared High and Low user-risk What If results before enabling it at 9:55:24 AM MDT.

I used Graph Explorer to confirm Tim compromised and verified **high / confirmedCompromised / adminConfirmedUserCompromised** at 10:39:53 AM MDT. During a new sign-in I was required to change the password and received a user-at-risk email; these observations have no separate prompt/email screenshots. Graph then verified **none / remediated / userPerformedSecuredPasswordChange** at 10:48:29 AM MDT. A subsequent fresh sign-in required MFA without another password change and retained Procurement.Reader and Procurement access.

Sign-in records initially appeared delayed. Later records included incomplete MFA, an expected Stay signed in interruption, and a successful post-remediation event. All captured CA-06 rows were Not Applied. I did not capture a distinct record directly attributing remediation to CA-06, measure ingestion latency, or test existing-session revocation. This was administrator-generated user risk, not an organic compromise or actual risky sign-in detection.

I restored CA-06 to Report-only at 11:10:17 AM MDT, stopped Flask, closed test Incognito windows, and signed out of Graph Explorer. I kept Tim's new password and Procurement access. Graph Explorer delegated-consent removal was not verified. The final Conditional Access state is **CA-00 through CA-03 On; CA-04 through CA-06 Report-only**. Security Defaults remained disabled. The October 30 export covered the original six policies; no CA-06 JSON export was collected.

See [Lab 17](../labs/17-identity-protection/README.md) for configuration, API requests, screenshots, and evidence limits.

## Trial Status

On October 30, 2026, I verified that my P2 free trial was Active, with **10 of 25 licenses assigned** and an expiration date of **November 7, 2026**. I disabled recurring renewal; the portal then stated that the trial would expire and the subscription would be canceled. A separate recurring-billing field displayed November 8, so I used November 7 as my preparation deadline. I have not recorded the post-expiry subscription state or feature behavior.

On October 30, I exported the six policies then present and confirmed their states at that time: CA-00 through CA-03 On, CA-04 and CA-05 Report-only. I verified that my regular administrator and Lab Recovery Administrator had direct, permanently active Global Administrator assignments, and tested a fresh recovery-account passkey sign-in and access to the Conditional Access page.

The planned transition to Security Defaults and the later post-expiry observations are not completed results. Security Defaults remained disabled during these P2 labs. Any future documentation will distinguish changes I make before expiry from effects I actually observe after licensing changes. The policy exports remain outside this public repository.

## Maintenance Notes

This is a snapshot of the environment documented through **October 31, 2026**, including Lab 09 PIM testing and cleanup and Lab 10 SAML SSO validation and assignment removal, Lab 11 OIDC/PKCE and session tests, Lab 12 OAuth API token-validation and read/write authorization tests, Lab 13 software OATH-TOTP registration, deletion, and replacement tests, Lab 14 entitlement-management request, approval, delivery, expiry, and fresh-sign-in denial tests, Lab 15 dynamic membership, department transfers, application-role authorization, and access removal tests, Lab 16 approval-controlled PIM group membership, application access, automatic expiry, and eligibility cleanup, and Lab 17 controlled user-risk creation, secured-password-change remediation, and final Report-only policy restoration. Subsequent lab changes may alter users, group membership, assignments, licenses, or Conditional Access policy states. Update this file when those configurations change, and keep detailed test evidence in each lab's own README.




