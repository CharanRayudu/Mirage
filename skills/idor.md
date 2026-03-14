# Skill: IDOR / Broken Object Level Authorization

## Scope & Safety
- Allowed only if target is in `scope_lock.json` and ROE permits authenticated testing.
- Requires two authorized test accounts (UserA, UserB).
- No exfiltration of sensitive data. Only confirm whether access control is enforced.

## Detection Heuristics
- Object IDs in path/query/body with predictable formats (sequential integers, UUIDs in URLs).
- Responses differ by ID but do not appear to enforce ownership/tenant checks.
- "403/404 on UI but 200 via direct API call" mismatch — client-side filtering without server-side checks.
- Same response structure regardless of which user makes the request.
- No server-side ownership validation visible in error messages.

## Safe Test Procedure (Two-Account Method)

1) **Create two authorized test users**: UserA and UserB (per ROE).
2) **With UserA**, access an object UserA owns and capture the request (HAR).
3) **Identify the object identifier field(s)** — look in path parameters, query strings, and request body.
4) **Repeat the same request as UserB** with UserA's object identifier.
5) **Record whether the server returns:**
   - ✅ Proper denial (403/404) — expected behavior
   - ❌ Data or behavior implying unauthorized access — candidate issue
6) **If candidate issue**: create Validator task to test boundary conditions:
   - Tenant switch (cross-tenant object access)
   - Role escalation (lower-privilege accessing higher-privilege objects)
   - Do NOT extract sensitive content — just confirm access control gap.

## Evidence Checklist
- [ ] HAR showing UserA request + response (with object ID)
- [ ] HAR showing UserB request + response (with same object ID)
- [ ] Notes on expected authorization policy
- [ ] Screenshot of any UI discrepancy (if applicable)
- [ ] List of tested endpoints and their access control behavior

## False-Positive Killers
- Caching (CDN/browser cache returning stale data)
- Public objects (some objects are intentionally shared)
- Soft-deleted objects returning different state
- Rate limiting masking as authorization failure
- Different response formats between API versions

## Remediation
- Enforce server-side ownership checks at every object access point.
- Avoid relying on client-side filtering or obscure IDs as security.
- Implement consistent authorization middleware.
- Log and alert on cross-user object access attempts.
