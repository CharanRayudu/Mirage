# SKILL: JavaScript Analysis

## Goal
Extract endpoints, API keys, secrets, and dependency information from publicly served JavaScript bundles.

## Scope & Safety
- Only analyze JS files served by in-scope targets.
- Do not execute or modify any scripts.
- Treat discovered secrets as "risk signals" — report, do not use.

## Methodology
1. Crawl target with katana to discover all JS file URLs.
2. Download JS files and analyze for:
   - Hardcoded API endpoints and paths
   - API keys, tokens, or secrets (regex patterns)
   - Third-party library versions (for supply chain assessment)
   - Source map references (`.map` files)
3. If source maps are publicly accessible, note as a finding (information disclosure).
4. Cross-reference discovered endpoints with the parameter discovery skill.

## Detection Heuristics
- Regex for API keys: `(api[_-]?key|token|secret|password)\s*[:=]\s*['"][^'"]+['"]`
- Endpoint patterns: `fetch\(`, `axios\.`, `XMLHttpRequest`, `/api/v`
- Source map indicators: `//# sourceMappingURL=`

## Output
- List of extracted endpoints, potential secrets (redacted), and dependency versions.
- Feed endpoints into `attack_graph.json` and dependencies into A03/A08 skills.

## Automation Hooks
- Emit `js_endpoint_extracted`, `js_secret_signal`, `js_dependency_found`.
