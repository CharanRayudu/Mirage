# Skill: <NAME>

## Scope & Safety
- Allowed only if target is in `scope_lock.json` and ROE permits this class of testing.
- No destructive actions. No data exfiltration. No credential reuse outside test accounts.

## What to Collect (Evidence Checklist)
- Requests/responses (HAR or raw).
- Screenshots (if UI).
- Exact endpoint + parameters involved.
- Account roles used (A vs B) and expected authorization boundary.

## Detection Heuristics
- <heuristic 1>
- <heuristic 2>
- <heuristic 3>

## Safe Test Procedure
1) Establish baseline behavior with authorized account.
2) Change only one variable per test.
3) Record responses and verify access-control outcome.
4) If suspicious, add a "Validator" task for safe confirmation.

## False-Positive Killers
- Caching / CDN variation
- Object-level RBAC rules
- Tenant boundaries
- Soft deletes
- Rate limiting / WAF responses

## Remediation Guidance
- Server-side authorization checks
- Deny-by-default
- Consistent object scoping
- Audit logs

## Report-Ready Writeup Template

```markdown
### [FINDING-ID] <Title>

**Affected Component:** <endpoint / feature>
**Severity:** <critical / high / medium / low / info>
**Confidence:** <0.0 – 1.0>

**Impact:**
<What could an attacker do?>

**Evidence:**
- <artifact path 1> — <what it shows>
- <artifact path 2> — <what it shows>

**Safe Reproduction Steps:**
1. <step>
2. <step>
3. <step>

**Suggested Fix:**
<specific remediation>
```
