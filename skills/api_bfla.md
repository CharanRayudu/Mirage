# SKILL: API5 — Broken Function Level Authorization (BFLA)

## Goal
Detect BFLA vulnerabilities where users can access functions beyond their authorization level.

## Scope & Safety
- Test with safe GET/OPTIONS requests to admin/privileged endpoints first.
- Do not execute admin functions. Only prove access is possible.
- Require HITL for any state-changing admin endpoint testing.

## OWASP API Top 10 Reference
- API5:2023 — Broken Function Level Authorization

## Methodology
1. Map API endpoints by function category (user, admin, internal, management).
2. Identify privileged endpoints (user management, config, billing, reports).
3. Attempt access as a low-privilege user or unauthenticated.
4. Check for HTTP method differences (GET allowed, POST/PUT also allowed?).

## Evidence
- Requests showing unauthorized access to privileged functions.
- Clear role matrix and expected vs actual authorization decisions.
