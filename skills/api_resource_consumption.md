# SKILL: API4 — Unrestricted Resource Consumption

## Goal
Detect missing rate limits, pagination abuse, and resource exhaustion vectors in APIs.

## Scope & Safety
- Do NOT perform denial-of-service testing.
- Test with minimal requests (5-10) to observe rate limiting presence/absence.
- Require HITL for any high-volume testing.

## OWASP API Top 10 Reference
- API4:2023 — Unrestricted Resource Consumption

## Methodology
1. Identify endpoints that return lists/collections.
2. Test pagination: does the API enforce maximum page sizes? Can you request `?limit=999999`?
3. Send 5-10 rapid requests to a single endpoint and observe if rate limiting kicks in.
4. Check for expensive operations (search, export, report generation) without throttling.
5. Look for GraphQL depth/complexity limits (if GraphQL is present).

## Evidence
- Response showing acceptance of unreasonable pagination values.
- Absence of rate-limit headers (X-RateLimit-*, Retry-After).
- Proof of missing complexity limits on GraphQL queries.
