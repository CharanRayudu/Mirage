# SKILL: A02 Security Misconfiguration (OWASP Top 10:2025)

## Goal
Detect externally observable misconfigurations (headers, debug endpoints, default pages, directory listing, permissive CORS, exposed admin surfaces).

## Scope & Safety
- Prefer passive scanning + low-impact checks.
- Do not brute-force credentials by default.
- Respect rate limits; treat scanning as "shared infrastructure".

## Granular Skills
- `cors_misconfig.md`, `open_redirect.md`, `path_traversal.md`

## Detection Heuristics
- Missing security headers (CSP/HSTS/XFO/etc) or insecure cookies.
- Accessible "/debug", "/metrics", "/actuator", "/swagger", "/api-docs", "/.env", "/.git/".
- Directory listing / static bucket listing / old build artifacts.

## Safe Test Steps
1. Run http probes (HEAD/GET) with metadata capture.
2. Run nuclei templates limited to safe categories (exposures/misconfiguration/info).
3. Check CORS behavior using simple preflight + benign origin headers (`{{ORIGIN}}`).
4. Verify whether misconfig is reachable without auth and within scope.

## Evidence
- Exact URL, status code, headers (redacted).
- Screenshot or stored response body snippet (redacted).
- Nuclei template id + timestamp.

## Automation Hooks
- Emit `misconfig_signal`, `evidence_captured`, `finding_candidate`.
