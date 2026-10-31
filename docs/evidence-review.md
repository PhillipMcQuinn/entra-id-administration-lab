# Evidence and Repository Security Review

**Review date:** October 31, 2026.

**Input snapshot:** commit `0a65c443c0970fd390e2b0fba8a75c78e4c7c31f`, before this review's documentation and ignore-rule edits.

I updated the October 30 review to include the recent evening labs, Lab 17, the application source, and reachable Git history. The findings below are the results of this screening, not a guarantee that the repository contains no sensitive information.

## Screenshot Rescreening

I ran Tesseract OCR across **all 251 current PNG/JPEG evidence images**, with no OCR command failures. I screened the extracted text for IPv4 patterns and recognizable credential formats, including private-key markers, GitHub/AWS token patterns, compact JWTs, and long bearer-token values. Loopback and unspecified addresses were excluded from the IP candidate list.

I also visually reviewed the 62 published images in the recent labs and inspected the detector candidates at full size:

| Evidence set | Images | Screening result |
|---|---:|---|
| Lab 15 — Dynamic groups | 22 | No IP-address or credential-pattern candidates |
| Lab 16 — PIM for Groups | 21 | No IP-address or credential-pattern candidates |
| Lab 17 — Identity Protection | 19 | No IP-address or credential-pattern candidates |
| Other current evidence | 189 | One browser-version IP candidate; one public-AppId false positive in the additional OCR/Gitleaks pass |

The candidate in [Lab 04 recovery verification](../labs/04-mfa/screenshots/06-recovery-verification.png) was the `Chrome/154.0.0.0` user-agent version, not a network address. I did not identify a public IP address in this screening. The recent images show configuration, fictional identities, selected claims, and event identifiers rather than raw authentication tokens.

I additionally passed the extracted OCR text through Gitleaks. It returned one generic-api-key candidate in [Lab 14 catalog resources](../labs/14-entitlement-management/screenshots/02-catalog-application-resource.png). Visual inspection confirmed that it was the truncated public application ID displayed beside `AppId`, not a credential. No confirmed secret was identified in that additional pass.

I compared the exact bytes of the two omitted Lab 17-era IP-bearing source images with the blobs in all reachable commits. Neither exact image blob was present. This does not prove that no altered copy could exist elsewhere. No screenshots were modified in this review.

OCR can miss small text, unusual fonts, cropped values, IPv6 addresses, QR/setup codes, and unrecognized credential formats. The visual review concentrated on Labs 15–17 and the IP/AppId candidates; it was not a full-size manual examination of every historical image.

## Full-History Secret Screening

I obtained a **non-shallow mirror** of the repository. Git enumerated **190 reachable commits**, with `main` as the sole advertised branch and no advertised tags. I downloaded **Gitleaks 8.30.1** from its official release and verified the archive against the published SHA-256 checksum.

I used the default detection rules, no repository allowlist or baseline, full output redaction, and `--ignore-gitleaks-allow` so inline allow comments would not suppress findings:

```sh
gitleaks git . --log-opts="--all --full-history" --redact=100 --ignore-gitleaks-allow --report-format=json --report-path=../history-gitleaks.json
gitleaks dir . --redact=100 --ignore-gitleaks-allow --report-format=json --report-path=../current-gitleaks.json
```

Both scans returned **three generic-api-key findings** and exit status **1**. I did not label those runs as zero-finding passes. I inspected the source context and classified all three as false positives:

| Finding | Classification |
|---|---|
| Lab 12 `app/src/app.js`, line 3 | Public API application/client ID assigned to a constant; not an API credential |
| Lab 12 `app/assets/app.js` | Bundled MSAL reference to `OIDC_DEFAULT_SCOPES`; not a token value |
| Lab 11 `app/assets/app.js` | Bundled MSAL reference to `OIDC_DEFAULT_SCOPES`; not a token value |

The history findings refer to the older uppercase folder names at their original commits. The current-file findings map to the corresponding lowercase paths. I did not suppress either rule or finding class.

Gitleaks' patch-scan log reported 126 processed commits, while Git enumerated 190 reachable commits. To avoid relying on that counter as proof of complete text coverage, I independently extracted **all 194 distinct UTF-8 text blobs** reachable from those commits and scanned that directory too. It returned the same three false positives. The **261 non-text/binary blobs** were excluded from that text cross-check; current evidence images received the separate OCR screening above.

**Outcome:** No confirmed credential was identified by the default-rule history scan, current-tree scan, historical-text-blob cross-check, and focused source inspection. This is a scoped result, not proof that no secret ever existed. Unreachable objects, deleted remote refs, external copies, private local files, and every historical image variant are outside the verified coverage. No Git history was rewritten or purged.

## Application Source and Ignore Rules

- **Lab 08 Flask application:** `CLIENT_SECRET` and `SESSION_SECRET` are read from local environment configuration; neither has a hardcoded credential fallback. The published `.env.example` contains replacement markers for secret values. Its existing application ID is public configuration, not a client secret.
- **Lab 12 API and browser client:** the source contains tenant, API, and client identifiers and retrieves public verification keys. I found no hardcoded client secret, signing private key, or live bearer token. The source tests generate disposable fixture keys at runtime.
- **Existing protection:** both Lab 08 and Lab 12 application `.gitignore` files contain `.env`. I verified the paths with `git check-ignore`; no actual `.env` file was tracked in the fetched history. The tracked `.env.example` is intentional.
- **Additional protection:** I added a root `.gitignore` covering `.env` and `.env.*` throughout the repository while preserving `.env.example` templates. Ignore rules help prevent future additions; they do not remove anything already committed.

This was credential screening and source inspection, not a penetration test or dependency-vulnerability audit. The local teaching servers remain unsuitable as production deployment templates.

## GitHub Secret Protection Status

On October 31, 2026, I verified the repository settings in the GitHub settings screenshot: **Secret Protection was enabled** (the available action was Disable), and **Push protection was On**.

The connected GitHub integration did not expose security-administration settings; I confirmed these settings through the owner-side screenshot rather than an API change.

I then reviewed the Secret scanning alerts screenshot on October 31, 2026. With the `is:open` filter displayed, GitHub showed **0 Open**, **0 Closed**, and **No secrets found**. This verifies that no unresolved alerts were displayed in that view at the time of review. It is a dated alert-view observation, not a guarantee that every credential format or future commit is free of secrets.

## Privacy and History Limits

I replaced the personal Free-tenant domain in current Markdown prose with the explicitly labelled placeholder `<free-lab-tenant>.onmicrosoft.com`. Tenant/object/application identifiers and fictional-user details remain where useful for test correlation; identifiers alone are not authentication credentials.

**The repository is not fully anonymized.** Existing screenshots and older commits can still disclose the original domain and its personal handle. This review neither rewrote history nor claimed to erase previously public information. A complete domain-redaction project would need separate image review and a deliberate history-rewrite plan.

## Tenant Controls Requiring Follow-up

The recovery administrator's passkey sign-in and permanently active Global Administrator assignment are documented. Automated alerts on each recovery-account sign-in and offline credential storage have **not** been verified. [Lab 07](../labs/07-conditional-access/README.md#recovery-account-controls-and-remaining-hardening) records these limits rather than presenting them as completed compensating controls.

The dedicated PIM test identity and its trial license were retained for optional repeat testing after the documented role cleanup. [Lab 09](../labs/09-privileged-identity-management/README.md#cleanup) records the retention rationale and the remaining account/license cleanup. No live Entra account, license, monitoring, or credential-storage changes were performed during this repository review.

## References

- [Gitleaks documentation and releases](https://github.com/gitleaks/gitleaks)
- [GitHub: Enable secret scanning and owner alerts](https://docs.github.com/en/code-security/how-tos/secure-your-secrets/detect-secret-leaks/enable-secret-scanning)
- [GitHub: Enable push protection](https://docs.github.com/en/code-security/how-tos/secure-your-secrets/prevent-future-leaks/enable-push-protection)
- [Microsoft: Manage emergency access accounts](https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/security-emergency-access)

[Return to portfolio](../README.md)
