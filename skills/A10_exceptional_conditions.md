# SKILL: A10 Mishandling of Exceptional Conditions (OWASP Top 10:2025)

## Goal
Find "fail open", inconsistent authorization on error paths, and sensitive leakage during abnormal conditions.

## Scope & Safety
- No DoS testing. Keep inputs small and low-rate.
- Avoid multi-megabyte payloads, deep recursion, or concurrency spikes.

## Granular Skills
- `business_logic.md`, `rate_limit_bypass.md`, `path_traversal.md`

## Detection Heuristics
- Different auth decision when upstream dependency fails (e.g., 5xx transforms into 200).
- Verbose stack traces in error responses.
- Retry logic causing duplicate operations.
- Boundary input causing unexpected state transitions.

## Safe Test Steps
1. Identify fragile edges: optional headers, malformed JSON, missing required params, expired tokens.
2. Send minimal malformed inputs: `{{MALFORMED_JSON}}` (tiny), `{{BOUNDARY_INT}}` (e.g., -1, 0, max-int placeholder).
3. Compare: status codes, error bodies, side effects, authorization outcomes.
4. If behavior suggests fail-open: require HITL to continue.

## Evidence
- Request/response pairs for normal vs exceptional cases, with timestamps and redaction.

## Automation Hooks
- Emit `exception_path_tested`, `fail_open_signal`, `finding_candidate`.
