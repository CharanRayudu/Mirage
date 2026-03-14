# Skill: CORS Misconfiguration

## Scope & Safety
- Allowed only if target is in `scope_lock.json` and ROE permits this class of testing.
- No destructive actions. No data exfiltration. No credential reuse outside test accounts.
- Test CORS policies safely by injecting origins, rather than exploiting the origin for Cross-Site Request Forgery directly on production data.

## What to Collect (Evidence Checklist)
- Requests/responses (HAR or raw) showing the `Origin` header sent and the `Access-Control-Allow-Origin` (ACAO) header returned.
- Ensure the `Access-Control-Allow-Credentials` (ACAC) header is evaluated if the endpoint handles sensitive PII or authentication mechanisms.
- The vulnerable endpoint and the HTTP method interacting with it.

## Detection Heuristics
- The server echoes the `Origin` header exactly as it was provided, even for arbitrary or untrusted domains (e.g., `Origin: https://evil.com` -> `ACAO: https://evil.com`).
- The `ACAO` header is set to `null` (`Origin: null` -> `ACAO: null`), which can be exploited via local HTML files or sandboxed iframes.
- The `ACAO` header is a wildcard `*` while authenticating sensitive requests.

## Safe Test Procedure
1) Establish a baseline behavior by sending a legitimate Request to the API without an Origin.
2) Replay the request injecting an unauthorized `Origin: https://evil.com`.
3) Check if `Access-Control-Allow-Origin: https://evil.com` is present in the response headers.
4) If ACAO is reflected, test if `Access-Control-Allow-Credentials: true` is also present.
5) If suspicious, add a "Validator" task for safe confirmation without stealing real tokens.

## False-Positive Killers
- The endpoint is designed to be public (e.g., public APIs, CDN assets) and does not handle sensitive data or use credentials.
- The reflection only occurs on safe subdomains that are explicitly allow-listed and not susceptible to takeover.
- The `Access-Control-Allow-Credentials: true` flag is missing on endpoints requiring authentication, rendering the ACAO reflection useless for credential theft.

## Remediation Guidance
- Never dynamically reflect the `Origin` header back into the `Access-Control-Allow-Origin` header without strict server-side validation.
- Maintain a strict allowlist of trusted origins that require cross-origin access.
- Only issue `Access-Control-Allow-Credentials: true` when explicitly needed, and never pair it with an overly broad or dynamically reflected origin policy.

## Report-Ready Writeup Template

```markdown
### [FINDING-ID] CORS Misconfiguration on <endpoint / feature>

**Affected Component:** <endpoint / feature>
**Severity:** <high / medium>
**Confidence:** <0.0 – 1.0>

**Impact:**
Because the application trusts arbitrary origins and allows credentials, an attacker can host a malicious website that forces authenticated users to make cross-origin requests. The attacker's script can read the responses containing sensitive PII or perform unauthorized actions on behalf of the victim.

**Evidence:**
- <artifact path 1> — Shows the HTTP request injecting `Origin: https://evil-domain.com`.
- <artifact path 2> — Shows the server's response returning `Access-Control-Allow-Origin: https://evil-domain.com` alongside `Access-Control-Allow-Credentials: true`.

**Safe Reproduction Steps:**
1. Intercept a request to `<endpoint>`.
2. Add or modify the header `Origin: https://evil.com`.
3. Send the request and observe the response headers.
4. Note that ACAO echoes the malicious origin and ACAC is set to `true`.

**Suggested Fix:**
Validate the `Origin` header against a strict, static allowlist of permitted domains. Do not dynamically reflect the origin. If the endpoint does not require cross-origin requests, disable CORS entirely or omit the `Access-Control-Allow-Origin` header.
```
