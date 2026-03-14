# SKILL: A04 Cryptographic Failures (OWASP Top 10:2025)

## Goal
Detect weak or missing transport protection, insecure cookie/session token handling, and crypto-adjacent data exposure visible from the outside.

## Scope & Safety
- No interception of other users' traffic.
- Only inspect your own sessions and app responses.

## Granular Skills
- `jwt.md`, `auth_testing.md`

## Detection Heuristics
- HTTP endpoints serving sensitive content without redirect to HTTPS.
- Missing HSTS where applicable.
- Cookies missing Secure/HttpOnly/SameSite where appropriate.
- Tokens stored/returned in risky places (URL params, referrers).

## Safe Test Steps
1. Test HTTP → HTTPS behavior (redirects, HSTS, mixed content observations).
2. Inspect Set-Cookie attributes for session cookies.
3. Check for sensitive data in URLs and responses (redact in logs).
4. JWT checks (delegate to jwt skill) for weak alg confusion patterns (placeholder only).

## Evidence
- Redirect chain, HSTS header presence/absence, cookie attributes.
- Redacted sample URLs showing sensitive material placement.

## Automation Hooks
- Emit `tls_posture_observed`, `cookie_flag_observed`, `finding_candidate`.
