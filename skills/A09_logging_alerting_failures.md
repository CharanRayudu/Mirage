# SKILL: A09 Security Logging & Alerting Failures (OWASP Top 10:2025)

## Goal
Identify externally observable logging/monitoring weaknesses and log-related exposures.

## Scope & Safety
- You generally cannot confirm "alerting exists" from black-box. Treat as "visibility risk signals."
- Do not inject harmful content; use a benign marker string only.

## Detection Heuristics
- Logs accessible via HTTP endpoints (e.g., /logs, /debug logs).
- Sensitive data in error responses (stack traces, tokens).
- Evidence that log data is reflected unsafely into responses (possible log injection vectors).

## Safe Test Steps
1. Check for exposed log/monitoring endpoints (passive + nuclei safe templates).
2. Trigger benign security-relevant events (e.g., failed login once) and observe: correlation IDs, response leakage.
3. Use a benign marker `{{LOG_MARKER}}` in a safe input field and observe if it appears unescaped in any user-visible log UI.

## Evidence
- URLs and response snippets (redacted), proof of exposure, reproduction notes.

## Automation Hooks
- Emit `logging_exposure_found`, `info_leak_signal`, `finding_candidate`.
