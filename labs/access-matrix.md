# Expected access matrix
| Stage | Department | Application access group | Effective app role | IT read | Procurement read |
|---|---|---|---|---|---|
| Before | No account | None | None | Denied | Denied |
| Joiner | IT | SG-GothamApp-IT-Readers | IT.Reader | Allowed | Denied |
| Mover | Procurement | SG-GothamApp-Procurement-Readers | Procurement.Reader | Denied | Allowed |
| Review applied | Procurement | None | None | Denied fresh | Denied fresh |
| Leaver | Procurement; blocked account | None | None | Denied fresh | Denied fresh |

Groups are assigned to app roles; Tim is not assigned directly. Organizational department groups alone do not grant this application access. Local sessions retain previously issued claims until expiry; record them separately.
