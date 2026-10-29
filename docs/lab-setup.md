# Microsoft Entra ID Lab Setup

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

### Environment 2 — Microsoft Entra ID P2 (Labs 06–09)

**Tenant:** `GothamLabz.onmicrosoft.com`  
**License:** Microsoft Entra ID P2

This environment was used for advanced IAM exercises requiring additional identity security and governance capabilities:

- Lab 06: Joiner–Mover–Leaver Identity Lifecycle Management
- Lab 07: Conditional Access and Identity Protection
- Lab 08: Enterprise Application Integration and Troubleshooting
- Lab 09: Privileged Identity Management

Labs 06–08 recorded two administrator accounts and seven standard user accounts, Microsoft Authenticator enrollment, Windows Hello passkeys for administrators, Conditional Access policies, and group-based application role assignments. Lab 09 added a dedicated PIM test account with an Entra ID P2 license and Microsoft Authenticator registration. Its eligible Helpdesk Administrator assignment was removed during cleanup.

### Environment Separation

Configuration settings, licenses, user accounts, and test results should be interpreted within their respective environments rather than assumed to apply across both tenants.

| Setting | Original setup record (October 5, 2026) | GothamLabz lab configuration (October 8–29, 2026) |
|---|---|---|
| Organization label | Gotham IAM Lab | Gotham IAM Lab / Gotham IT Labs; Gotham Labs in Lab 09 |
| Tenant type | Workforce | Microsoft Entra workforce identity lab |
| Recorded tenant domain | `phillipmcquinngmail.onmicrosoft.com` | `GothamLabz.onmicrosoft.com` |
| Licensing | Microsoft Entra ID Free | Microsoft Entra ID P2 assigned for lab accounts |
| Operating system | Windows 11 | Windows workstation used for the local application exercises |
| Browser | DuckDuckGo recorded at setup | Browser sessions used for administration, sign-in, and Windows Hello tests; exact browser varies by test |
| Authenticator | Microsoft Authenticator | Microsoft Authenticator; Windows Hello passkeys on administrator accounts |
| Admin center | [Microsoft Entra admin center](https://entra.microsoft.com) | [Microsoft Entra admin center](https://entra.microsoft.com) |

The two tenant domains represent separate environments, not a domain rename or migration. Labs 01–05 retain their original Free-tenant context; Labs 06–09 use GothamLabz.

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
| `SG-CA-Lab-Users` | Scope lab-user Conditional Access testing |
| `Managers` | Group referenced in an earlier Conditional Access manager/device-control exercise |

Group membership **does not automatically grant permissions to arbitrary applications**. The Gotham Access Lab enterprise application was configured with group-to-application-role assignments, which linked the reader groups to `IT.Reader` and `Procurement.Reader` respectively. The application required users to be assigned. Individual lab READMEs record the membership and access tests.

## Authentication and Security Configuration

### Authentication methods

- Microsoft Authenticator registration was checked for the GothamLabz accounts.
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

The recovery administrator was excluded from enforced policies in the documented configuration. Four policies were **On** and two were **Report-only** at the time of Lab 07 testing. A report-only result or What If calculation is not the same as an enforced sign-in result. Consult [Lab 07](../labs/07-Conditional-Access/README.MD) for individual evidence.

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

See [Lab 08](../labs/08-Enterprise%20Application%20Integration/README.MD) for the detailed procedure, observations, and evidence.

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

See [Lab 09](../labs/09-Privileged-Identity-Management/README.MD) for the complete findings and screenshot evidence. Audit timestamps reproduce the portal's displayed values; a timezone label was not captured.

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
| Joiner–Mover–Leaver | Reader permissions changed and denied on removal; offboarding tests recorded | [Lab 06](../labs/06-Joiner-Mover-Leaver/README.MD) |
| Entra ID P2 and MFA | Licensing and MFA registration checked for GothamLabz test accounts | [Lab 07](../labs/07-Conditional-Access/README.MD) |
| Conditional Access | Four policies On, two Report-only; selected successful sign-in logs reviewed | [Lab 07](../labs/07-Conditional-Access/README.MD) |
| Enterprise application RBAC | Procurement Allowed; IT Inventory Denied for Procurement Reader | [Lab 08](../labs/08-Enterprise%20Application%20Integration/README.MD) |
| Assignment revocation | Fresh sign-in denied with AADSTS50105; existing-session access persisted until sign-out | [Lab 08](../labs/08-Enterprise%20Application%20Integration/README.MD) |
| PIM activation and revocation | Password reset succeeded only while the role was active; denied before activation, after manual deactivation, and after automatic expiry | [Lab 09](../labs/09-Privileged-Identity-Management/README.MD) |
| PIM approval and audit | Pending request did not grant password-reset access; approval, activation, and expiry audit evidence captured | [Lab 09](../labs/09-Privileged-Identity-Management/README.MD) |

## Evidence and Security Handling

- Screenshots use fictional employees and training resources.
- Descriptions distinguish **configured**, **What If / Report-only**, **observed**, and **enforced/tested** results.
- Screenshots may not prove every configuration action completed; the relevant lab notes any evidence limitations.
- Passwords, recovery codes, authentication QR codes, access/refresh tokens, private keys, application secrets, and session cookies must not be published.
- Review screenshots for personal account information and sensitive browser content before uploading.

## Maintenance Notes

This is a snapshot of the environment documented through **October 29, 2026**, including Lab 09 PIM testing and cleanup. Subsequent lab changes may alter users, group membership, assignments, licenses, or Conditional Access policy states. Update this file when those configurations change, and keep detailed test evidence in each lab's own README.
