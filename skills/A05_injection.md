# SKILL: A05 Injection (OWASP Top 10:2025)

## Goal
Systematically test for injection classes using non-destructive probes and placeholders, escalating only with HITL.

## Scope & Safety
- Default: detection via benign markers and minimal payloads.
- Any aggressive fuzzing, time-based probes, sqlmap, ZAP active scan, or high-rate ffuf requires HITL.

## Granular Skills
- `xss.md`, `command_injection.md`, `rce.md`, `path_traversal.md`

## Detection Heuristics
- Reflected input in HTML/JSON without encoding.
- Error messages revealing parser/engine details.
- Parameter behaviors inconsistent with normalization (e.g., special chars break logic).
- Suspicious sinks: file paths, template params, command-ish params, JSON parser edges.

## Safe Test Steps
1. Build parameter inventory (katana + captured traffic).
2. Use placeholder probes: XSS: `{{XSS_PROBE}}`, SQLi: `{{SQLI_PROBE}}`, CMDi: `{{CMDI_PROBE}}`.
3. Compare response diffs (status, length, reflection points).
4. Only after HITL: targeted deeper validation using specialized tooling.

## Evidence
- Parameter list, request/response diffs, reflection location, safe reproduction steps.

## Automation Hooks
- Emit `param_inventory_built`, `injection_signal`, `finding_candidate`.
