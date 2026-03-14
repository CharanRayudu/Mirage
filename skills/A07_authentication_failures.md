# SKILL: A07 Authentication Failures (OWASP Top 10:2025)

## Goal
Assess authentication and session management weaknesses without brute forcing.

## Scope & Safety
- No credential stuffing by default.
- Any rate-limit testing must be scoped and throttled; prefer synthetic low-rate checks.

## Granular Skills
- `auth_testing.md`, `jwt.md`, `oauth_misconfig.md`

## Detection Heuristics
- Session fixation indicators (session id unchanged across login).
- Weak logout (session remains valid).
- Password reset/token reuse logic flaws.
- Username enumeration via timing/error text.

## Safe Test Steps
1. Record baseline session lifecycle: before login / after login / after logout / after password change.
2. Check token rotation and invalidation.
3. Test reset flow invariants with placeholders: `{{RESET_TOKEN}}`, `{{MAGIC_LINK}}` (do not steal tokens).
4. Validate consistent error messaging (avoid high-volume enumeration).

## Evidence
- Session token changes across lifecycle.
- Clear reproduction steps and constraints.

## Automation Hooks
- Emit `session_lifecycle_observed`, `auth_signal`, `finding_candidate`.
