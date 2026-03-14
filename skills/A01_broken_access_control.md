# SKILL: A01 Broken Access Control (OWASP Top 10:2025)

## Goal
Identify and validate broken access control issues (IDOR/BOLA, privilege escalation, CSRF-class behaviors, SSRF mapped under A01) using black-box methods.

## Scope & Safety (Non-negotiable)
- Only test in-scope hosts/paths in `programs/<program>/scope.yaml`.
- Default to read-only requests (GET/HEAD) and low-rate probing.
- Any action that modifies state (POST/PUT/DELETE), touches admin functions, or attempts SSRF to internal IP ranges requires HITL approval.

## Granular Skills
- `idor.md`, `auth_testing.md`, `jwt.md`, `ssrf.md`, `cors_misconfig.md`, `rate_limit_bypass.md`, `business_logic.md`

## Detection Heuristics
- ID patterns: sequential IDs, UUIDs, base64-ish tokens, slug+id combos.
- "Soft" authorization: UI hides links but API still accepts requests.
- Inconsistent authorization across methods: GET locked down, PATCH not; list endpoint restricted but detail endpoint open.

## Safe Test Steps
1. **Inventory endpoints** — Use passive capture (Burp/mitmproxy) while browsing. Use katana/gau/wayback to find hidden endpoints.
2. **Build role matrix** — At minimum: unauthenticated, normal user, any available secondary role.
3. **IDOR/BOLA checks (read-only first)** — Replay the same request with different object id (`{{OBJECT_ID_OTHER_USER}}`) or same id but different auth context. Observe: 200 vs 403/404, data differences, property-level leaks.
4. **Function-level auth checks** — Enumerate "admin-like" endpoints (e.g., /admin, /internal, /manage). Try safe GET/OPTIONS first.
5. **SSRF mapped under A01 (detection-only by default)** — Identify fetcher features (URL previews, webhooks, PDF generation, image proxy). Use a benign controlled endpoint you own: `{{SSRF_CANARY_URL}}`. Confirm only that the server *attempted* an outbound request. Do NOT target internal IPs, metadata services, or localhost unless explicitly in scope.

## Evidence Checklist
- Request/response pairs for each role and object id tested.
- Clear statement of "expected vs observed authorization decision".
- Redacted sensitive fields; preserve enough to prove impact.
- If SSRF: proof of server-initiated request to canary endpoint (time + path).

## Automation Hooks
- Emit `endpoint_discovered`, `auth_context_created`, `access_control_tested`, `finding_candidate`.
- Update `attack_graph.json`: nodes = endpoints, objects, roles; edges = `tested_as`, `leaks`, `bypasses`.
