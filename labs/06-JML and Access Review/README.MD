# Lab 6 — Complete JML and access review (P2)
Status: Pending execution. Request approvals are simulated lab approvals; access-review decisions will be executed in Entra using fictional accounts.

Employee: Tim Drake, WE006, `TimDrake@GothamLabz.onmirosoft.com`. Department IT → Procurement. Application Gotham Access Lab. Use dedicated **assigned security groups** `SG-GothamApp-IT-Readers` and `SG-GothamApp-Procurement-Readers` so reviews cannot remove unrelated department access. Department groups from earlier labs can remain separate organizational memberships.

## Prerequisites
Confirm P2 seats for the reviewed user and designated reviewer and appropriate licensing for premium app access. Configure [the application](../../apps/gotham-access/README.md). Use separate admin/employee browser profiles. Record administrator role used; use an appropriate application/group administrator for configuration and an Identity Governance Administrator for reviews as required.

In Enterprise applications → Gotham Access Lab → Properties, enable Assignment required. Assign `SG-GothamApp-IT-Readers` to **IT Reader** and `SG-GothamApp-Procurement-Readers` to **Procurement Reader** under Users and groups. Remove any direct Tim assignments left from the Free version. Use direct group membership; nested membership is not the test path. The app reads the roles claim rather than trusting department text.

## Joiner
1. Confirm Tim does not exist and has no access assignments. Unauthenticated `/it` and `/procurement` should return 401; record this as unauthenticated access, not an employee login denial.
2. Complete SIM-JML-001 in [approvals](approvals.md) before execution. Create Tim, set IT department, require password change at first sign-in, assign the required license, and add Tim to the IT application group (plus organizational IT group if used).
3. Capture membership and group-to-role assignment. Complete fresh sign-in/MFA as required; expect IT 200 and Procurement 403. Record actual role claim, logs and screenshots.

## Mover
4. Complete SIM-JML-002. Capture before permissions; change department to Procurement, remove IT application/department memberships, and add Procurement memberships. Do not assign Tim directly to either app role.
5. Record previous-session behavior. Then use Fresh Entra sign-in; expect Procurement 200 and IT 403. Allow for group/role propagation and document timing; stale claims are not a passing fresh-session result.

## P2 access review checkpoint
6. Before offboarding, follow [access-review.md](access-review.md) to review the Procurement application group. Deny Tim's access with a fictional reason that a temporary assignment has ended. Complete and apply the review, then prove the membership and effective app role are gone. This deliberately removes access ahead of leaver controls and tests review enforcement.
7. Attempt fresh app sign-in after propagation: with no other assignment, Assignment required should deny application sign-in. Record the actual outcome/error. If sign-in still succeeds, inspect direct assignments, other assigned groups and cached sessions.

## Leaver
8. Complete SIM-JML-003. Confirm both app-group memberships and any direct assignments are absent; remove organizational department memberships. Block Tim's account and revoke Entra sign-in sessions.
9. Test a fresh sign-in in a private browser and record the actual disabled-account failure. Test the previous app session immediately and after its five-minute expiry. Entra revocation does not invalidate this app's local cookie immediately.
10. Complete [results](results.md). Keep the user blocked until screenshots/logs are collected, then delete the fictional account if desired. Remove test credentials once no longer needed.

[Access matrix](access-matrix.md) · [Approvals](approvals.md) · [Evidence](screenshots/README.md)

This is a manual JML scenario with group-based authorization and an actual access review, not automated Lifecycle Workflows. [Licensing](https://learn.microsoft.com/en-us/entra/id-governance/licensing-fundamentals).
