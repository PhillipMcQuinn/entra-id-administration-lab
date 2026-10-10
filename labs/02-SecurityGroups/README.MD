# Lab 02: Security Group Administration

## Objective

Practice administering Microsoft Entra ID **Assigned** security groups for fictional departments. Verify group creation and membership, simulate an employee transfer between departments, and use group membership views and audit logs to confirm changes.

## Status

**Completed — October 6, 2026.** The exercise included a department transfer and subsequent restoration of the test user's original department and group memberships.

## Environment

| Setting | Value |
|---|---|
| Lab environment | Gotham IAM Lab (foundational labs) |
| Microsoft Entra tenant | `phillipmcquinngmail.onmicrosoft.com` |
| License | Microsoft Entra ID Free |
| Administrator role used | Global Administrator |
| Date performed | October 6, 2026 |

All employee names and department scenarios in this exercise are fictional.

## Group Design

| Group name | Group type | Membership type | Intended purpose |
|---|---|---|---|
| `SG-Executive-Employees` | Security | Assigned | Executive department employees |
| `SG-IT-Employees` | Security | Assigned | IT department employees |
| `SG-Procurement-Employees` | Security | Assigned | Procurement department employees |
| `SG-Lab-Test-Users` | Security | Assigned | Accounts used for lab testing |

These groups organize users for potential access assignments. **Group membership alone does not establish access to an application or resource**; authorization requires a corresponding resource assignment or access control configuration.

### Department membership plan

| Fictional employee | Department group |
|---|---|
| Bruce Wayne | `SG-Executive-Employees` |
| Lucius Fox | `SG-IT-Employees` |
| Dick Grayson | `SG-IT-Employees` |
| Selina Kyle | `SG-Procurement-Employees` |

The table records the planned department mapping. The included screenshots document selected group membership views; they are not presented as independent screenshots of every row above.

## Prerequisites

- Fictional employee accounts in the original Entra ID Free lab tenant.
- Administrator permission to create security groups and modify their memberships.
- Existing membership information for comparison before and after the transfer.
- Access to Microsoft Entra ID group membership views and audit logs.

## Part 1: Create and Review Security Groups

Created the required department security groups using **Security** group type and **Assigned** membership. Group names and descriptions identify their intended departments. Reviewed the resulting group listings.

**Evidence:**

![Security group creation and listing](screenshots/01-Security-Groups-Create.png)

## Part 2: Assign and Verify Group Members

Added users to their intended department groups and checked membership using the group members view. The exercise also confirmed that membership could be reviewed from an individual user's profile.

**Observed result:** The selected Procurement and Executive group membership lists displayed assigned users.

**Evidence:**

![Procurement group members](screenshots/02-Procurement-members.png)

![Executive group members](screenshots/03-executive-members.png)

## Part 3: Simulate a Department Transfer

**Scenario:** Dick Grayson moves from the IT department to Procurement.

### 1. Review the original employee profile

Reviewed Dick Grayson's existing department information and group membership before changing his department.

**Evidence:**

![Employee profile before transfer](screenshots/04-User-Profile.png)

### 2. Update the department attribute

Changed Dick's **Department** attribute to **Procurement**.

**Observed result:** Updating the department attribute did **not** automatically update membership in these **Assigned** security groups. Manual group membership changes were required.

**Evidence:**

![Employee profile after department update](screenshots/05-User-Profile-Update.png)

### 3. Remove old membership and add new membership

Removed Dick from `SG-IT-Employees`, added him to `SG-Procurement-Employees`, and reviewed the resulting group membership lists.

**Observed result:** Dick appeared in the Procurement group and no longer appeared in the IT group after the manual changes.

**Evidence:**

![Procurement group membership after transfer](screenshots/06-procurement-members.png)

![IT group membership after transfer](screenshots/07-it-members-after-transfer.png)

## Part 4: Review Group Administration Audit Logs

Reviewed available Microsoft Entra ID audit events for group administration and membership changes.

**Observed result:** Audit records showed individual group changes. These records provide a way to investigate the operation performed and associated audit details.

**Evidence:**

![Group administration audit events](screenshots/08-group-audit.png)

![Group membership change audit events](screenshots/09-group-Change-Audit.png)

## Validation Results

| Test | Observed result | Outcome |
|---|---|---|
| Create security groups | Required groups were created and appeared in the directory | Passed |
| Assign members | Users appeared in the applicable group membership views | Passed |
| Change employee department | Assigned group memberships did not automatically change | Confirmed |
| Remove IT group membership | Dick was removed from `SG-IT-Employees` | Passed |
| Add Procurement membership | Dick was added to `SG-Procurement-Employees` | Passed |
| Review audit events | Group administration and membership events were available for review | Passed |
| Restore initial configuration | Dick's department and group memberships were returned to the original IT configuration | Reported complete |

**Scope:** This lab verified group membership administration. It did **not** test downstream application permissions, dynamic group membership, or automatic HR-driven provisioning.

## Issues and Troubleshooting

No unexpected errors were reported during the exercise. The primary behavior investigated was that changing a user's **Department** attribute did not automatically change memberships in security groups configured with **Assigned** membership.

This behavior required manual removal from the former department group and manual addition to the new department group.

## Cleanup

After completing the transfer tests, restored Dick Grayson's original lab configuration:

- **Department:** IT
- **Member of:** `SG-IT-Employees`
- **Not a member of:** `SG-Procurement-Employees`

The original lab notes report that this cleanup was completed. A separate post-cleanup screenshot was not listed among the nine evidence images in this README.

## Lessons Learned

- **Assigned security groups require explicit membership administration.** Editing a user's department attribute does not automatically move that user between Assigned groups.
- **Department transfers involve more than profile updates.** Old group membership should be removed and new membership assigned as appropriate to avoid retaining unnecessary entitlements.
- **Membership should be validated from multiple views.** The group's member list and the user's group membership view help confirm changes.
- **Audit logs support accountability and troubleshooting.** They can record changes, their status, timestamps, and actor information, depending on the audit event.
- **Group membership and application authorization are not synonymous.** This exercise establishes directory group administration; separate resource tests are needed to demonstrate application access.

---

**Environment note:** Labs 01–05 use the original `phillipmcquinngmail.onmicrosoft.com` Entra ID Free tenant. Labs 06–08 use the separate GothamLabz Entra ID P2 tenant.
