# SKILL: API SSRF (Server-Side Request Forgery via APIs)

## Goal
Detect SSRF vulnerabilities in API endpoints that accept URLs or fetch remote resources.

## Scope & Safety
- Detection-only by default. Use a benign canary URL you control.
- Do NOT target internal IPs, cloud metadata endpoints, or localhost unless explicitly in scope.
- Require HITL before any escalation.

## OWASP API Top 10 Reference
- API7:2023 — Server Side Request Forgery (also consolidated under OWASP A01 in 2025)

## Methodology
1. Identify API endpoints that accept URL parameters (webhooks, callbacks, image fetchers, PDF generators, preview features).
2. Submit a benign canary URL (`{{SSRF_CANARY_URL}}`) that you control.
3. Monitor your canary server for incoming requests from the target.
4. If callback is received: note the source IP, user-agent, timing, and request path.
5. Do NOT attempt to read internal resources or cloud metadata.

## Evidence
- Proof of server-initiated outbound request to your canary (timestamp, source IP, path).
- The API endpoint and parameter that triggered the SSRF.
- Clear statement of what was NOT tested (internal pivoting, metadata access).
