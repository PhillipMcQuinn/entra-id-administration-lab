# P2 group access review — execution walkthrough
Status: Pending. This reviews one assigned group and uses basic P2 capabilities; do not select advanced Governance-only inactive-user scoping or affiliation recommendations.

1. After the mover tests, capture Tim's Procurement app-group membership and a fresh successful Procurement test. Confirm no direct app-role assignment or alternative assigned group supplies the same access.
2. Open ID Governance → Access reviews → New access review. Choose Teams + Groups, select **SG-GothamApp-Procurement-Readers**, and review all member users in this small lab group.
3. Name it `AR-Gotham-Procurement-TemporaryAccess`. Select a designated, appropriately licensed reviewer account you control; use a separate reviewer identity from Tim. Set a one-time review, start today, short duration (for example one day). Record actual dates/timezone.
4. Require justification. Turn **Auto apply results off** for the first exercise so you can inspect decisions before application. Set no-response behavior to **No change**. Capture the configuration and actual available settings.
5. Sign in as the reviewer through My Access (`https://myaccess.microsoft.com`) or the provided review link. Deny Tim with justification: “Simulated temporary Procurement assignment ended; remove application access.” Capture decision and submission time. If another authorized lab member exists, approve that member and explain their ongoing need; do not create extra users unless licensed.
6. As the review administrator, verify the submitted decision, stop the review early if supported or wait for its configured end, then **Apply results**. Record completion/application status and audit evidence. A submitted denial alone is not proof access was removed.
7. Verify Tim's group membership is removed; verify no direct assignment or other group preserves access. After propagation, attempt fresh app sign-in. Expect assignment-required denial; record the actual code. Also record stale local-session behavior.
8. Continue the leaver sequence. Preserve the review result/export with sensitive fields redacted.

## Review record
| Field | Observed value |
|---|---|
| Review name / ID | Pending |
| Scope and user count | Pending |
| Reviewer / license coverage | Pending |
| Start / end (UTC) | Pending |
| Tim decision / justification / time | Pending |
| Results applied time and status | Pending |
| Membership before / after | Pending |
| Fresh access test / actual error | Pending |
| Evidence filenames | Pending |

[Create a review](https://learn.microsoft.com/en-us/entra/id-governance/create-access-review) · [Complete/apply results](https://learn.microsoft.com/en-us/entra/id-governance/complete-access-review).
