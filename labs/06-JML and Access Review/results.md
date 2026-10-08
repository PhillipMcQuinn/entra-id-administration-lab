# Observed results
Status: Pending. Do not replace expected outcomes with claimed results until tested.

## Before/after assignments
| Request | Before department/app group/effective role | After department/app group/effective role | Account enabled? | Evidence |
|---|---|---|---|---|
| SIM-JML-001 | Pending observation | Pending observation | Pending | Pending |
| SIM-JML-002 | Pending observation | Pending observation | Pending | Pending |
| SIM-JML-003 | Pending observation | Pending observation | Pending | Pending |

## Tests
| Test | Expected | Observed/error/status | UTC time | Evidence | Verdict |
|---|---|---|---|---|---|
| Before: account lookup and unauthenticated routes | No account; routes 401 | Pending | Pending | Pending | Not run |
| Joiner: IT route | 200 | Pending | Pending | Pending | Not run |
| Joiner: Procurement route | 403 | Pending | Pending | Pending | Not run |
| Mover: fresh Procurement route | 200 | Pending | Pending | Pending | Not run |
| Mover: fresh IT route | 403 | Pending | Pending | Pending | Not run |
| Mover: previous session | Record stale/current roles | Pending | Pending | Pending | Not run |
| Leaver: fresh Entra sign-in | Denied; record actual code | Pending | Pending | Pending | Not run |
| Leaver: previous session immediately | Record behavior | Pending | Pending | Pending | Not run |
| Leaver: previous session after expiry | Local routes 401 | Pending | Pending | Pending | Not run |

Record browser/session used, sign-in log correlation ID, assignment propagation delay and discrepancies. Add relative screenshot links after uploading each file. No nonexistent screenshot links are included here.

## Access review tests
| Check | Expected | Observed | UTC time / evidence | Verdict |
|---|---|---|---|---|
| Before review | Procurement group and fresh access | Pending | Pending | Not run |
| Reviewer decision | Deny with justification | Pending | Pending | Not run |
| Apply results | Completed; Tim removed from group | Pending | Pending | Not run |
| Fresh application sign-in | Denied; no remaining assignment | Pending | Pending | Not run |

Record license coverage, group-to-role mapping, direct-assignment check and propagation delays.
