# Rules of Engagement (ROE)

## Authorization

- **Only test targets explicitly listed in `scope.yaml`.**
- Written authorization is **mandatory** before expanding scope beyond localhost.
- Unauthorized scanning or exploitation is illegal — period.

## Boundaries

| Action Category | Default | HITL Required? |
|---|---|---|
| Passive Recon (headers, status, routes) | ✅ Allowed | No |
| Authenticated Testing (with test accounts) | ✅ Allowed | No |
| Active Fuzzing (parameter fuzzing, brute-force) | ❌ Disabled | Yes |
| Exploitation (PoC execution) | ❌ Disabled | Yes |
| Data Exfiltration | ❌ Never | N/A |
| Lateral Movement | ❌ Never | N/A |
| Persistence / Backdoors | ❌ Never | N/A |

## Evidence Standards

- Every finding must reference an artifact path (HAR, screenshot, tool output).
- Hypotheses without evidence must be labeled as such and queued for validation.
- Reports must only cite evidence-backed findings.

## Data Handling

- Raw HTTP traffic may be stored locally for evidence purposes.
- Secrets (API keys, tokens, passwords) must be redacted in reports.
- Findings database (`findings.db`) stays local — never push to remote without review.

## Rate Limits

- Default HTTP rate: **2 requests/second**
- Default tool timeout: **300 seconds**
- Browser automation timeout: **900 seconds**

## Incident Response

If testing causes unintended disruption:
1. **Stop all automated testing immediately.**
2. Document what happened (timestamps, commands, outputs).
3. Notify the target owner per their incident response process.
4. Preserve all artifacts for review.

## Notes

- This ROE applies to all agents in the system (Planner, Executor, Reflector, Specialists).
- Agents must check `scope_lock.json` before every action — no exceptions.
- When in doubt, **stop and ask the human operator**.
