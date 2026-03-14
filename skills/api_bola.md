# SKILL: API1 — Broken Object Level Authorization (BOLA)

## Goal
Detect BOLA/IDOR vulnerabilities in API endpoints by testing whether object-level authorization is enforced.

## Scope & Safety
- Only test with read-only requests (GET) by default.
- Use your own test accounts and objects. Do not access other real users' data.
- Any state-changing BOLA test (PUT/DELETE) requires HITL.

## OWASP API Top 10 Reference
- API1:2023 — Broken Object Level Authorization

## Methodology
1. Identify API endpoints that accept object identifiers (IDs, UUIDs, slugs).
2. Authenticate as User A, note object IDs belonging to User A.
3. Authenticate as User B (or unauthenticated), replay requests with User A's object IDs.
4. Compare responses: if User B can read/modify User A's objects, BOLA is confirmed.

## Evidence
- Request/response pairs showing unauthorized object access.
- Object IDs tested, user contexts used, expected vs actual authorization.
