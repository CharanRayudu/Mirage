# SKILL: A03 Software Supply Chain Failures (OWASP Top 10:2025)

## Goal
Surface *externally verifiable* supply-chain risk signals: outdated internet-facing components, exposed build artifacts, public CI/CD leaks, and version-to-CVE correlations, without exploit attempts.

## Scope & Safety
- No exploitation of known CVEs.
- Only OSINT against public resources tied to the target (public repos, public images, public package metadata).
- Treat results as "risk candidates" until validated by safe, target-consented checks.

## Detection Heuristics (black-box)
- Service version banners or fingerprints match known vulnerable versions.
- Publicly accessible build artifacts: sourcemaps, JS bundles with dependency versions, SBOMs, container tags.
- Public CI misconfig: exposed runners, leaked tokens (do NOT download/abuse secrets; report safely).

## Safe Test Steps
1. Fingerprint versions (nmap service detection; HTTP headers; JS bundle metadata).
2. Use web research to find: public release notes / versions, public CVE advisories for that component/version.
3. Validate exposure non-destructively: confirm the specific version is deployed (multiple independent signals), confirm the affected endpoint is reachable in scope.

## Evidence
- Multiple independent version signals.
- Source links (public advisories).
- Clear statement: "risk signal" vs "confirmed vulnerability".

## Automation Hooks
- Emit `component_fingerprint`, `cve_osint_linked`, `risk_candidate`.
