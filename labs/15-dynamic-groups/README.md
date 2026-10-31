# Lab 15 — Dynamic Groups and Automated Department Transfers

**Date completed:** October 30, 2026  
**Environment:** GothamLabz.onmicrosoft.com — Microsoft Entra ID P2 free trial  
**Application:** Gotham Access Lab  
**Test account:** Tim Drake

## Outcome

I connected department-based dynamic security groups to application roles and verified that changing Tim Drake's Department automatically changed his group membership and application access. I tested Procurement access, transferred him to IT, transferred him back to Procurement, and then used a nonmatching department to remove access. A fresh sign-in after removal failed with `AADSTS50105`.

I performed all administration and testing myself, using my administrator account and Tim's fictional account in separate browser sessions. I changed the Department attribute during the transfer tests; I did not manually edit Tim's dynamic memberships or change the application assignments between tests.

## Scenario and Baseline

I reused the Flask/OIDC application from [Lab 08](../08-enterprise-application-integration/README.md). Its protected pages check `IT.Reader` and `Procurement.Reader`, and its enterprise application requires assignment. The temporary direct assignment from [Lab 14](../14-entitlement-management/README.md) had already expired and been removed.

Tim began with Department **Procurement** and no membership in either original assigned application reader group. I created separate dynamic groups while retaining the original groups and application assignments. The new rules match users by department; they are not restricted to Tim.

![Tim Department set to Procurement before testing](screenshots/01-tim-procurement-baseline.png)

I kept the shared runnable application in [Lab 08’s `app/` folder](../08-enterprise-application-integration/app/README.md), including dependency and local configuration instructions.

## 1. I created and validated the dynamic rules

I created two cloud security groups with **Dynamic User** membership and configured the following rules. I assigned each group separately to its corresponding application role.

| Dynamic security group | Membership rule | Gotham Access Lab role |
|---|---|---|
| `DG-GothamApp-IT-Readers` | `(user.department -eq "IT")` | IT Reader (`IT.Reader`) |
| `DG-GothamApp-Procurement-Readers` | `(user.department -eq "Procurement")` | Procurement Reader (`Procurement.Reader`) |

With Tim still in Procurement, I used **Validate Rules** against his account. The IT rule returned a red nonmatch and the Procurement rule returned a green match. I treated these as rule-evaluation results and separately waited for actual group membership.

![IT rule validation does not match Tim](screenshots/02-it-rule-validation.png)

![Procurement rule validation matches Tim](screenshots/03-procurement-rule-validation.png)

The Procurement group initially showed **0 members** and processing **Not started**, even though the rule matched Tim. I verified his directly assigned Entra ID P2 license was Active. I left processing enabled and waited for the initial population. I later confirmed his Procurement dynamic membership on the user Groups page.

The group was created at **3:11 PM MDT** and I captured Tim's membership at approximately **5:03 PM MDT**. I did not continuously monitor initial processing, so these observations do not establish its exact completion time. The later department changes were much faster.

![Initial Procurement group overview shows zero members and processing Not started](screenshots/04-initial-processing-not-started.png)

![Tim has an active directly assigned Entra ID P2 license](screenshots/05-tim-p2-license.png)

## 2. I verified the group-to-role assignments

During setup, selecting both groups without a role left **Assign** disabled. I completed the assignments separately so each group received the correct role. I checked the audit-log modified properties for the group name and application role value.

| Assignment I verified | Audit timestamp (UTC) |
|---|---|
| DG-GothamApp-IT-Readers → IT.Reader | 2026-10-30 21:30:17 |
| DG-GothamApp-Procurement-Readers → Procurement.Reader | 2026-10-30 21:30:38 |

![Audit properties associate the IT dynamic group with IT.Reader](screenshots/06-it-group-role-audit.png)

![Audit properties associate the Procurement dynamic group with Procurement.Reader](screenshots/07-procurement-group-role-audit.png)

## 3. I tested the Procurement baseline

I confirmed that Tim belonged to the Procurement dynamic group and `SG-CA-Lab-Users`, with no IT reader membership. I started the local Flask application and signed in as Tim in an Incognito session.

The identity page displayed only `Procurement.Reader`. Procurement allowed access and IT Inventory returned **Forbidden**.

![Actual Procurement dynamic membership before transfers](screenshots/08-procurement-membership-baseline.png)

![Baseline identity displays only Procurement.Reader](screenshots/09-baseline-procurement-role.png)

![Baseline IT Inventory access is forbidden](screenshots/10-baseline-it-forbidden.png)

![Baseline Procurement access is allowed](screenshots/11-baseline-procurement-allowed.png)

## 4. I transferred Tim from Procurement to IT

At **5:12 PM MDT**, I saved Department **IT**. Within my observed one-minute window, the IT dynamic group appeared and the Procurement dynamic group disappeared from Tim's Groups page. `SG-CA-Lab-Users` remained.

I closed all Incognito windows and opened a fresh session before signing in again. The identity page displayed only `IT.Reader`. IT Inventory allowed access, and Procurement returned **Forbidden** because Tim lacked `Procurement.Reader`.

![Tim automatically joined IT and left Procurement](screenshots/12-transfer-it-membership.png)

![Fresh session displays only IT.Reader](screenshots/13-transfer-it-role.png)

![IT Inventory access is allowed after transfer](screenshots/14-it-access-allowed.png)

![Procurement access is forbidden after transfer to IT](screenshots/15-procurement-forbidden.png)

## 5. I tested the reverse transfer

At **5:17 PM MDT**, I saved Department **Procurement**. I observed the Procurement dynamic membership return and the IT dynamic membership disappear within one minute.

After closing all Incognito windows and signing in in a new one, I confirmed `Procurement.Reader` was the only role. Procurement allowed access and IT Inventory was forbidden again.

![Procurement dynamic membership returned and IT membership disappeared](screenshots/16-return-procurement-membership.png)

![Fresh session after reverse transfer displays Procurement.Reader only](screenshots/17-return-procurement-role.png)

![IT Inventory is forbidden after reverse transfer](screenshots/18-return-it-forbidden.png)

![Procurement is allowed after reverse transfer](screenshots/19-return-procurement-allowed.png)

## 6. I removed access through a nonmatching department

At **5:21 PM MDT**, I saved Department **Lab-NoAccess**, which matched neither reader rule. Within one minute, I observed that both dynamic reader groups were absent. Only `SG-CA-Lab-Users` remained in Tim's group list.

I closed all Incognito windows and attempted a fresh application sign-in. Entra returned **AADSTS50105**, stating that Tim lacked an assigned access path. This verified denial at the application assignment gate after automatic membership removal.

![Tim has neither dynamic reader membership after nonmatching department change](screenshots/20-no-reader-membership.png)

![Fresh application sign-in fails with AADSTS50105](screenshots/21-unassigned-sign-in-denied.png)

## Validation Matrix

| Department state I tested | Actual reader membership | Role shown after fresh sign-in | IT Inventory | Procurement |
|---|---|---|---|---|
| Procurement baseline | Procurement dynamic group only | Procurement.Reader only | Forbidden | Allowed |
| IT, saved 5:12 PM MDT | IT dynamic group only | IT.Reader only | Allowed | Forbidden |
| Procurement, saved 5:17 PM MDT | Procurement dynamic group only | Procurement.Reader only | Forbidden | Allowed |
| Lab-NoAccess, saved 5:21 PM MDT | Neither dynamic reader group | Sign-in blocked with AADSTS50105 | Application sign-in blocked | Application sign-in blocked |

I observed each of the three test membership changes within one minute of saving the department. These are manually observed portal intervals, not exact backend timestamps or a service guarantee. I did not continuously probe the application during processing or establish whether any transient overlap occurred.

## Cleanup and Final State

I restored Department **Procurement** and observed the Procurement dynamic group return within one minute. The final group list showed that group and `SG-CA-Lab-Users`, with no IT dynamic membership. I retained both dynamic groups, their rules, and their application-role assignments. I stopped Flask and closed the test Incognito windows after testing.

![Final restored Procurement dynamic membership with CA lab group retained](screenshots/22-restored-procurement-membership.png)

## Evidence Limits and Lessons

- I verified actual memberships, displayed role claims, allowed and forbidden application pages, and a fresh-sign-in failure. I did not independently inspect or validate raw token signatures in this exercise.
- I collected audit properties for the group-to-application-role assignments. I did not collect correlated audit events for every Department edit and automatic membership change, or a correlated sign-in-log export for the final denial.
- I used fresh application sessions after membership changes. I did not test termination of an existing Flask session or revocation of previously issued tokens. The membership timing therefore does not measure existing-session access removal.
- I restored final membership but did not repeat application authorization tests after the cleanup restoration; the reverse-transfer tests had already verified Procurement authorization.
- I kept the local `.env`, session secret, and client secret private. I did not modify account enabled state or Conditional Access policies to produce the denial.

I learned to distinguish rule validation from completed membership processing, group membership from application-role assignment, and directory changes from the roles held by an existing session. The Department attribute became an access-control input, so controlling who can edit that attribute matters as much as configuring the rules correctly.

## References

- [Create or update a dynamic membership group](https://learn.microsoft.com/en-us/entra/identity/users/groups-create-rule)
- [Dynamic membership rule syntax](https://learn.microsoft.com/en-us/entra/identity/users/groups-dynamic-membership)
- [Validate dynamic membership rules](https://learn.microsoft.com/en-us/entra/identity/users/groups-dynamic-rule-validation)
- [Manage dynamic group processing](https://learn.microsoft.com/en-us/entra/identity/users/manage-dynamic-group)

[Back to portfolio](../../README.md)

