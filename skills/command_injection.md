# Skill: Command Injection (CMDi)

## Scope & Safety
- Allowed only if target is in `scope_lock.json` and ROE permits this class of testing.
- No destructive actions. No data exfiltration. No credential reuse outside test accounts.
- **NEVER** use disruptive or state-mutating commands (e.g., `rm -rf`, `shutdown`).
- Always use benign diagnostic commands (e.g., `id`, `whoami`, `hostname`, `sleep`) to prove execution concisely.

## What to Collect (Evidence Checklist)
- Requests/responses (HAR or raw) showing the injected payload and the server's output containing the command result.
- If it's a Blind Command Injection, capture timing data showing the server intentionally pausing (e.g., using `sleep 5`).
- Exact endpoint + parameters/headers utilized for the injection.

## Detection Heuristics
- The server echoes standard output of a system command directly back to the HTTP response (e.g., printing the output of `id`).
- The application response is delayed exactly as prescribed by an injected time-delay payload (e.g., `sleep 10` takes 10 seconds).
- The application evaluates unexpected metacharacters (`|`, `;`, `&`, `$()`) differently, occasionally triggering verbose system errors.

## Safe Test Procedure
1) Establish a baseline behavior for the target parameter with typical legitimate inputs.
2) Inject basic metacharacters accompanied by benign commands (e.g., `; id`, `| whoami`, `& hostname`).
3) Analyze the response body to see if the system command's output is included.
4) If the output is not visible (Blind CMDi), test a timing payload (e.g., `; sleep 5`) and measure if the HTTP response takes at least ~5 seconds longer than the baseline.
5) If suspicious, add a "Validator" task to securely confirm the finding without escalating privileges.

## False-Positive Killers
- The delayed response is caused by network latency or backend processing inconsistencies, not the `sleep` command. Prove via varied time metrics (5s, 10s) to correlate correctly.
- The metacharacter is sanitized contextually before the command executes, but the input is reflected back into the response verbatim.
- The input is passed into an ORM or safe API library instead of a system shell interpreter.

## Remediation Guidance
- Avoid passing user-supplied input directly into system shells (e.g., `os.system()`, `child_process.exec()`).
- Use language-specific safe API methods that do not invoke a shell environment (e.g., parameterizing commands or `subprocess.run(["cmd", "arg"])`).
- Implement absolute allow-lists for inputs intended to map directly to systems commands.
- Apply rigorous input sanitization, stripping all executable metacharacters.

## Report-Ready Writeup Template

```markdown
### [FINDING-ID] OS Command Injection on <endpoint / feature>

**Affected Component:** <endpoint / feature>
**Severity:** <critical / high>
**Confidence:** <0.0 – 1.0>

**Impact:**
An attacker can execute arbitrary operating system commands with the privileges of the executing application runtime. This can lead to full system compromise, data exfiltration, or lateral movement within the hosting network.

**Evidence:**
- <artifact path 1> — Demonstrates the HTTP request containing the `| id` payload.
- <artifact path 2> — Showcases the vulnerable HTTP response containing the injected output footprint `uid=` or `gid=`.

**Safe Reproduction Steps:**
1. Send a request to `<endpoint>` modifying the `command` parameter to `valid_input | id`.
2. Inspect the HTTP response body.
3. Observe that the command output of the Linux `id` utility is successfully echoed back without sanitization.

**Suggested Fix:**
Refactor the application behavior to rely entirely on safe administrative APIs provided by the programming language instead of invoking OS shells directly. Utilize strict allowlisting for arguments if OS invocation is unavoidable, and avoid directly concatenating user input into shell strings.
```
