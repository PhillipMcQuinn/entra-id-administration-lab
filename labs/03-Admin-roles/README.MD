# Lab 03: Administrative Roles and Least Privilege

## Objective

Assign a limited administrator role to a dedicated test account,
verify allowed and restricted actions, and remove the role after testing.

## Status

Complete

## Environment

- Tenant: Gotham IAM Lab
- License: Entra ID-FREE
- Date performed: October 6, 2026
- Test administrator: helpdesk-test
- Assigned role: Helpdesk Administrator
- Assignment scope: Tenant
- Target employee: Dick Grayson — standard user with no admin roles

## Scenario

The help desk needs to reset employee passwords.
The test administrator receives Helpdesk Administrator rather than
Global Administrator because the task does not require full tenant control.

## Prerequisites

- Dedicated helpdesk-test account exists.
- Dick Grayson exists as a standard test user.
- The role-assignment administrator can manage Entra role assignments.
- Existing roles on helpdesk-test have been recorded.
- Separate browser sessions are available for each account.

## Part 1: Review the Role

Review Microsoft's description of Helpdesk Administrator.

Document:
- Why this role was selected.
This role grants necassary privlidges to perform tasks for other non administrative users. 
- Which actions it permits.
Users with this role can change passwords, invalidate refresh tokens, manage service requests, and monitor service health.
- Which actions fall outside its permissions.
Cannot change the credentials or reset MFA for members and owners of a role-assignable group or other administrators.
- Any restrictions based on the target user's administrator role.
none for this lab.

Reference:
https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/permissions-reference

## Part 2: Assign the Role

Using the role-assignment administrator:

1. Open Roles & admins in the Entra admin center.
2. Select Helpdesk Administrator.
3. Add helpdesk-test as an assignment.
4. Verify the assignment and scope.

Evidence:

![Helpdesk Administrator assignment](screenshots/01-role-assignment.png)

## Part 3: Test an Allowed Action

Using a separate browser session, sign in as helpdesk-test.

1. Open Dick Grayson's user account.
2. Reset his password.
3. Do not save or publish the temporary password.
4. Verify the password reset by signing in as Dick in another session.
5. Record any password-change prompts and the actual result.

Evidence:

![Password reset confirmation](screenshots/02-password-reset.png)

## Part 4: Test a Restricted Action

While signed in as helpdesk-test:

1. Attempt to assign an administrator role to a separate test account.
2. Record whether the controls are unavailable or permission is denied.
3. Capture the displayed message without sensitive information.

Expected result:
Helpdesk Administrator cannot assign Entra administrator roles.

Do not switch accounts to complete the restricted action.
The purpose is to demonstrate the permission boundary.

Evidence:

![Role assignment restricted](screenshots/03-restricted-action.png)

## Part 5: Review Audit Logs

Using the main lab administrator, locate available events for:
- Adding the role assignment.
- Resetting the employee password.

Record the timestamp, initiating account, target, and result.

A denied action might not produce the same audit evidence as a
successful change. Document what you actually find.

Evidence:

![Administrative audit events](screenshots/04-audit-events.png)

## Part 6: Remove the Role and Retest

Using the role-assignment administrator:

1. Remove Helpdesk Administrator from helpdesk-test.
2. Confirm the role assignment no longer appears.
3. Sign out of the test administrator's session.
4. Sign in again and repeat the password-reset attempt.
5. Record the outcome and any observed propagation delay.

Expected result:
The test account can no longer reset another user's password,
provided it has no other role granting that permission.

Evidence:

![Role removed](screenshots/05-role-removed.png)

![Password reset restricted after removal](screenshots/06-retest.png)

## Validation Results

| Test | Expected result | Actual result |
|---|---|---|
| Role assignment | Helpdesk Administrator assigned at tenant scope | Roles show under "Assigned Roles" in the users profile, and in the Roles & admins <selected role> "assignments"  |
| Standard-user password reset | Reset succeeds | Successfully reset a standard users password with no issues or errors. |
| Employee sign-in | New password works | User had to reset password upon login, temp password that was assigned from helpdesk-test worked as expected. |
| Administrator role assignment | Unavailable or denied | Cant complete task, the option to add assignments is grayed out. |
| Role removal | Assignment no longer appears | After removal of the role, total roles assigned is 0 in the users assigned roles |
| Password reset after removal | Unavailable or denied | Helpdesk-test can no longer complete this task as the user longer has any administrative roles assigned to the account. |
| Audit review | Successful changes have supporting events | Audit longs confirm all roles added and removed to the users profile, password changes to Dick Grayson's account. |

## Troubleshooting

Record:
- Symptom or error.
- Account and role used.
- Investigation.
- Resolution.
- Retest result.
no errors occurred during this lab. All Tasks were successful.

## Cleanup

- Remove the temporary role assignment.
- Confirm helpdesk-test has no unintended administrator roles.
- Restore the employee account for future labs.
- Retain redacted screenshots only.

## Lessons Learned

Complete after testing:

- Why Helpdesk Administrator fit the task.
This role grants a user access to change other standard user permissions and password without granting global administrator access.
- The difference between group membership and an administrator role.
Memberships define what users belong together while roles provide privileges to complete tasks for other users.
- How allowed and denied actions demonstrate least privilege.
If a user does not have "privileged" roles, than tasks remain grayed out preventing an action from being taken. 
- What happened after the role was removed.
After the Helpdesk Administrator was removed from the test account, all administrative tasks like changing passwords became grayed out preventing the test user from executing that task.

Helpdesk-test account was removed upon completion of the lab.
