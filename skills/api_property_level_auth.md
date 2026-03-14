# SKILL: API3 — Broken Object Property Level Authorization

## Goal
Detect cases where API responses expose properties users shouldn't see, or accept property modifications users shouldn't make.

## Scope & Safety
- Read-only testing by default. Only observe excessive data exposure.
- Do not attempt mass assignment without HITL approval.

## OWASP API Top 10 Reference
- API3:2023 — Broken Object Property Level Authorization

## Methodology
1. Compare API responses across different user roles for the same object.
2. Look for sensitive properties returned to low-privilege users (email, role, internal IDs, PII).
3. For mass assignment testing (with HITL): send additional properties in PUT/PATCH requests and observe if they are accepted.
4. Check if filtering is client-side only (UI hides fields but API returns them).

## Evidence
- Response body diffs showing excessive data exposure per role.
- Property names that were accepted in write operations unexpectedly.
