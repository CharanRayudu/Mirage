# SKILL: Parameter Discovery

## Goal
Identify input parameters (query, body, header, cookie) across discovered endpoints for injection and access control testing.

## Scope & Safety
- Use passive observation and crawling output first.
- Only send safe GET requests with benign parameter values for validation.
- Do not fuzz parameters without HITL approval.

## Methodology
1. Parse katana/gau/waybackurls output for URL query parameters.
2. Analyze HTTP responses for form fields, JSON keys, and hidden inputs.
3. Review API documentation (if publicly available) for parameter schemas.
4. Categorize parameters by type: identifiers, search terms, file paths, auth tokens, flags.

## Detection Heuristics
- Sequential/predictable IDs → IDOR candidate
- File path parameters → path traversal candidate
- Template/eval-like parameters → injection candidate
- Unvalidated redirect parameters → open redirect candidate

## Output
- Parameter inventory with endpoint, name, type, and risk category.
- Feed into `attack_graph.json` as `parameter` nodes linked to `endpoint` parents.

## Automation Hooks
- Emit `parameter_discovered`, `parameter_risk_categorized`.
