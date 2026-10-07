# Microsoft Entra ID Lab Setup

## Purpose

All employee identities are fictional. This environment is used
exclusively for training.

## Environment

| Setting | Configuration |
|---|---|
| Organization name | Gotham IAM Lab |
| Tenant type | Workforce |
| License | Microsoft Entra ID Free
| Tenant domain | phillipmcquinngmail.onmicrosoft.com |
| Admin portal | https://entra.microsoft.com |
| Operating system | Windows 11 |
| Browser | DuckDuckGo |
| Authentication app | Microsoft Authenticator |
| Setup date | 2026-10-05 |

## Administrator Accounts

| Account | Assigned role | Purpose |
|---|---|---|
| Phillip McQuinn | Global Admin | Lab configuration |

Administrative accounts are separate from fictional employee accounts.

Passwords, recovery codes, authentication QR codes, and access tokens
are not stored in this repository.

## Fictional Test Users

The following records are example lab data.

| Display name | Username | Job title | Department | Manager |
|---|---|---|---|---|
| Bruce Wayne | BruceWayne | Chief Executive Officer | Executive | Phillip McQuinn |
| Alfred Pennyworth | AlfredPennyworth | Assistant Executive | Executive | Bruce Wayne
| Lucius Fox | LuciusFox | IT Director | IT | Bruce Wayne |
| Barbara Gordon | BarbaraGordon | Systems Administrator | IT | Lucius Fox |
| Dick Grayson | DickGrayson | Support Specialist | IT | Lucius Fox |
| Selina Kyle | SelinaKyle | Procurement Specialist | Procurement | Bruce Wayne |

Usernames use the lab tenant's .onmicrosoft.com domain.

Additional fictional attributes:
- Employee ID: unique identifier, such as WE001.
- Hire date: fictional date recorded for onboarding scenarios.

## Security Groups

| Group name | Membership type | Purpose |
|---|---|---|
| SG-IT-Employees | Assigned | Practice IT department membership |
| SG-Executive-Employees | Assigned | Practice department transfers |
| SG-Lab-Test-Users | Assigned | Identify accounts used for testing |
| SG-Procurement-Users | Assigned | Practice Procurement department membership |

Group membership alone does not provide application access.
Application permissions are documented in the relevant lab.

## Tools

- Microsoft Entra admin center: user, group, and role administration.
- Microsoft Authenticator: test-user MFA registration.
- GitHub: documentation and redacted evidence.

## Initial Configuration Checklist

Mark items complete only after performing and verifying them.

- [X] Confirm access to the correct tenant.
- [X] Record the actual license edition.
- [X] Review the administrator account's assigned role.
- [X] Create fictional test users.
- [X] Populate department and job-title attributes.
- [X] Assign managers.
- [X] Create assigned-membership security groups.
- [X] Add test users to the appropriate groups.
- [X] Document the current authentication configuration.

## Verification

| Check | Expected result | Actual result | Evidence |
|---|---|---|---|
| Tenant access | Correct organization is displayed | Tenant Displays correctly | Complete |
| User creation | Test user appears in Users | all Users Show Created | Complete |
| User attributes | Department and job title match lab records | User Attributes Display accurately | Complete |
| Group membership | Test user appears in the intended group | Group Assignments appear accurately | Complete |
| Test-user sign-in | User can sign in successfully | Users can sign in successfully | Complete |


## Licensing and Scope

Support multifactor authentication, unlimited SSO across any SaaS app, basic reports, and self-service password change for cloud users.
Manage users and groups in the cloud.

## Evidence Handling

Screenshots and reports use fictional employee data.
Identifying tenant details are redacted where appropriate.

No passwords, tokens, recovery codes, or authentication QR codes
are published.
