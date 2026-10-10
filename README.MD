# Microsoft Entra ID Administration & IAM Security Portfolio

This repository documents my hands-on Identity and Access Management (IAM) training in personal Microsoft Entra ID lab environments. It focuses on practical administration, identity lifecycle operations, access control, multifactor authentication, Conditional Access, and enterprise application troubleshooting.

Each lab records the scenario, configuration steps, observed outcomes, troubleshooting, and available screenshot evidence. These exercises are **personal lab experience**, not work performed in a production enterprise tenant.

## Featured Lab Results

| Area | Hands-on result |
|---|---|
| Identity lifecycle | Tested joiner, mover, leaver, role changes, access reviews, and access removal with a fictional employee account |
| Conditional Access | Configured six policies; enabled four and retained two in Report-only mode |
| Administrator security | Registered and tested Windows Hello passkeys and verified an enforced phishing-resistant MFA requirement |
| Identity Protection | Evaluated Medium- and High-risk sign-in conditions using the What If simulator; no actual risky sign-in event was generated |
| Enterprise applications | Configured app roles, security group assignments, and assignment-required access for Gotham Access Lab |
| Authorization troubleshooting | Demonstrated an existing session retaining access after group removal, followed by a fresh sign-in denied with **AADSTS50105** |

## Lab Projects

| Lab | Project | Focus |
|---|---|---|
| 01 | [Employee Onboarding and Offboarding](labs/01-User-Lifecycle/README.MD) | User creation, attributes, group membership, sign-in, and offboarding |
| 02 | [Security Groups](labs/02-SecurityGroups/README.MD) | Group creation, assignment, and membership administration |
| 03 | [Administrative Roles](labs/03-Admin-roles/README.MD) | Entra directory roles and administrative permissions |
| 04 | [MFA Registration and Recovery](labs/04-MFA/README.MD) | Microsoft Authenticator, security information, and authentication methods |
| 05 | [Sign-in Troubleshooting](labs/05-Troubleshooting/README.MD) | Diagnosing authentication failures through Entra sign-in logs |
| 06 | [Joiner–Mover–Leaver Identity Lifecycle](labs/06-Joiner-Mover-Leaver/README.MD) | Department transfer, group-based application access, access review, and offboarding |
| 07 | [Conditional Access and Identity Protection](labs/07-Conditional-Access/README.MD) | MFA, phishing-resistant authentication, legacy-auth blocking policy, and risk simulations |
| 08 | [Enterprise Application Integration and Troubleshooting](labs/08-Enterprise-Application-Integration/README.MD) | OpenID Connect, app roles, My Apps visibility, consent, RBAC, and assignment-based access revocation |

## Lab Environments

The portfolio includes exercises performed during different stages of my Entra ID learning environment. Earlier labs documented a **Microsoft Entra ID Free** configuration. Subsequent GothamLabz exercises used **Microsoft Entra ID P2** features.

### GothamLabz P2 environment

| Component | Lab configuration |
|---|---|
| Tenant domain | `GothamLabz.onmicrosoft.com` |
| License | Microsoft Entra ID P2 |
| Test identities | Nine accounts, including two administrator accounts |
| Authentication | Microsoft Authenticator and device-bound Windows Hello passkeys |
| Access control | Assigned security groups, application roles, and Conditional Access |
| Test application | Gotham Access Lab — locally hosted Python Flask web application integrated with Microsoft Entra ID |

For historical setup details, see [Lab Setup](docs/lab-setup.md). The original setup documentation may describe an earlier tenant or licensing stage and should be read in that context.

## IAM Skills Practiced

- **Identity lifecycle:** account creation, attribute updates, group management, joiner–mover–leaver processes, and offboarding.
- **Access control:** least privilege, role-based access control (RBAC), enterprise app assignments, and access reviews.
- **Authentication:** Microsoft Authenticator MFA, Windows Hello passkeys, and phishing-resistant authentication strengths.
- **Conditional Access:** policy targeting and exclusions, Report-only evaluation, staged enforcement, and sign-in investigation.
- **Identity Protection:** sign-in risk-based What If simulations using Entra ID P2.
- **Enterprise applications:** application roles, delegated Microsoft Graph permissions, administrator consent, OpenID Connect integration, and sign-in failures such as `AADSTS50105`.
- **Troubleshooting and evidence:** Entra sign-in logs, audit investigation, session behavior, screenshots, and documented limitations.

## Evidence and Scope

Evidence is organized within each lab's `screenshots/` folder and linked from that lab's README. Results are explicitly differentiated:

- **Verified configuration:** a setting or assignment shown in the Entra portal.
- **What If simulation:** a policy-matching test, not a real enforced authentication event.
- **Enforced sign-in:** an observed authentication event with an applicable Conditional Access result.
- **Observed without screenshot:** a result recorded during hands-on testing without a separate image.
- **Not tested:** a control without a corresponding real-world event, such as an actual legacy-client block or risky sign-in.

All employees, scenarios, and organization names in the labs are fictional. Secrets, passwords, authentication tokens, and local `.env` settings are not intended for publication.

## About This Portfolio

I built these labs to expand on my enterprise technical support experience and demonstrate practical skills relevant to IAM Analyst, Identity Security Analyst, Access Management Analyst, and Identity Operations roles.

[LinkedIn](https://www.linkedin.com/in/phillipmcquinn/)
