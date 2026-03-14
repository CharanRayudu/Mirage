# SKILL: API9 — Improper Inventory Management / API Exposure

## Goal
Discover undocumented, deprecated, or shadow API endpoints that may lack security controls.

## Scope & Safety
- Passive discovery only. Use OSINT, crawling, and historical sources.
- Do not brute-force API paths—use intelligent pattern matching.

## OWASP API Top 10 Reference
- API9:2023 — Improper Inventory Management

## Methodology
1. Compare documented API (OpenAPI/Swagger) with actually discovered endpoints.
2. Look for API versioning patterns: `/v1/`, `/v2/`, `/v3/` — are old versions still accessible?
3. Search for staging/test/internal APIs via OSINT (gau, waybackurls, GitHub search).
4. Check for API endpoints that return different schemas than documented.
5. Look for debug/test endpoints left in production.

## Evidence
- List of undocumented or deprecated endpoints that are still accessible.
- Version comparison showing old APIs without security controls.
- OSINT sources where shadow APIs were discovered.
