# SKILL: A08 Software or Data Integrity Failures (OWASP Top 10:2025)

## Goal
Detect cases where untrusted code/data is treated as trusted: risky third-party scripts, missing integrity signals, unsafe deserialization-like behaviors visible externally.

## Scope & Safety
- No malicious file uploads; use safe inert files if upload testing is allowed.
- No exploitation of deserialization; only detect suspicious behavior safely.

## Granular Skills
- `prototype_pollution.md`, `file_upload.md`

## Detection Heuristics
- Third-party scripts without SRI when appropriate for the context.
- Update/download endpoints lacking basic integrity signals.
- File upload acceptance without basic validation signals (content-type confusion, stored file behavior).

## Safe Test Steps
1. Crawl JS assets; extract third-party origins.
2. Check for SRI attributes where static third-party scripts are used.
3. For uploads (if in scope): upload a harmless file (`{{SAFE_TEST_FILE}}`), observe storage behavior and access controls.
4. Record and report integrity gaps with minimal risk.

## Evidence
- Asset URLs, SRI presence/absence, upload behavior, access control on stored files.

## Automation Hooks
- Emit `asset_integrity_checked`, `upload_integrity_checked`, `finding_candidate`.
