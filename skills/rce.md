# Skill: Remote Code Execution (RCE) via Serialization or Template Injection

## Scope & Safety
- Allowed only if target is in `scope_lock.json` and ROE permits this class of testing.
- No destructive actions. No data exfiltration. No credential reuse outside test accounts.
- **NEVER** use disruptive or state-mutating commands (e.g., `rm -rf`, `shutdown`).
- Always use benign diagnostic computations (e.g., `{{ 7*7 }}`, `<% out.print(7*7); %>`) or safe diagnostic system calls (e.g., `id`, `whoami`, `hostname`, `sleep`) to prove execution concisely and non-destructively.

## What to Collect (Evidence Checklist)
- Requests/responses (HAR or raw) showing the injected payload and the server's output containing the computed or executed result.
- If it's a Blind RCE, capture timing data showing the server intentionally pausing (e.g., using a language-specific sleep construct) or an OOB interaction (DNS resolution) if the infrastructure allows safe logging.
- Exact endpoint, HTTP Method, and data format (JSON, XML, FormData) utilized for the injection.

## Detection Heuristics
- The application evaluates dynamic template expressions (SSTI) reflecting mathematical operations (e.g., `{{ 7*7 }}` returning `49`).
- Deserialization of untrusted data (Java, Python Pickle, .NET) triggers known gadget chains or throws verbose errors indicating object instantiation failures.
- Server-side execution engines (Node VM, PHP `eval()`) process arbitrary language expressions maliciously passed via API parameters.

## Safe Test Procedure
1) Establish a baseline behavior for the target parameter with typical legitimate inputs.
2) For Template Injection (SSTI): Inject a basic math expression like `${7*7}` or `{{7*7}}`. If `49` is returned, escalate to safe context discovery payloads (e.g., `{{ self }}` or `{{ config }}`).
3) For Insecure Deserialization: Identify serialized data formats (e.g., base64 encoded Java objects starting with `rO0AB`, XML, YAML). Inject a safe exception-throwing gadget chain or an OOB DNS lookup (if ROE permits).
4) Analyze the response body or out-of-band monitoring logs to confirm execution.
5) If suspicious, add a "Validator" task to securely confirm the finding without escalating privileges.

## False-Positive Killers
- The templating engine is running entirely client-side (Client-Side Template Injection, CSTI), which is essentially XSS, not RCE.
- The arithmetic payload is executed by a safe, sandboxed expression evaluator intended for mathematical operations, not arbitrary code execution.
- The deserialized object fails safe type-casting upstream, preventing the malicious gadget chain from ever executing its final sink.

## Remediation Guidance
- Never pass user-supplied input directly into an execution sink like `eval()`, `exec()`, or template parsers.
- Use safe serialization formats like JSON instead of robust language-native binaries (e.g., Python `pickle`, Java serialization).
- If native deserialization is required, strictly enforce strong object type allowlisting.
- Run the web application runtime with the principle of least privilege in strong sandboxing environments.

## Report-Ready Writeup Template

```markdown
### [FINDING-ID] Severe Remote Code Execution on <endpoint / feature>

**Affected Component:** <endpoint / feature>
**Severity:** <critical>
**Confidence:** <0.0 – 1.0>

**Impact:**
An attacker can execute arbitrary code within the application environment. This leads to profound consequences including complete system compromise, uncontrolled data exfiltration, lateral network movement, and total loss of confidentiality, integrity, and availability.

**Evidence:**
- <artifact path 1> — Demonstrates the HTTP request containing the Server-Side Template Injection (SSTI) payload `{{ 7*7 }}`.
- <artifact path 2> — Showcases the HTTP response successfully evaluating the expression and echoing the integer `49` to the client.

**Safe Reproduction Steps:**
1. Send a request to `<endpoint>` modifying the `name` parameter to `{{ 7*7 }}`.
2. Inspect the HTTP response body.
3. Observe that the template engine parsed the user input as code and returned the evaluated result `49`.

**Suggested Fix:**
Cease utilizing user input as an argument for rendering templates. Ensure that user input is treated as context-aware text strings or variables passed to the rendering context, rather than raw template directives.
```
