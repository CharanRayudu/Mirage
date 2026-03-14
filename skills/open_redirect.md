# Skill: Open Redirect

## Scope & Safety
- Allowed only if target is in `scope_lock.json` and ROE permits this class of testing.
- No destructive actions. No data exfiltration. No credential reuse outside test accounts.
- Do not blindly scrape domains or perform mass redirection checks against out-of-scope targets.

## What to Collect (Evidence Checklist)
- Requests/responses (HAR or raw) showing the unvalidated redirect.
- The parameter or header manipulated (e.g., `?next=`, `?returnUrl=`, `Host` header).
- Screenshot of the browser redirection if UI interaction is possible.
- Evidence that the redirect goes to an external, untrusted, or attacker-controlled domain (e.g., `example.com` redirecting to `evil.com`).

## Detection Heuristics
- The server responds with an HTTP 3xx status code (e.g., 301, 302) and a `Location` header containing the injected payload.
- Client-side JavaScript reads a URL parameter and assigns it to `window.location` or similar without proper origin validation.

## Safe Test Procedure
1) Identify input vectors commonly used for redirection (e.g., login flows, logout flows, interstitial pages).
2) Inject a benign, distinct, but external domain (e.g., `http://example.org`) into the parameter.
3) Observe the response. If the server returns a `Location` header pointing to `http://example.org`, it indicates an open redirect.
4) Provide a valid path as a baseline, and change only the suspicious parameter.
5) If suspicious, add a "Validator" task for safe confirmation.

## False-Positive Killers
- The application redirects safely to relative paths or pre-approved, allow-listed domains (e.g., subdomains of the target).
- The application strips out the scheme (`http://`) or domain and only redirects to the path.
- Server-side validation throws a 400 Bad Request when an external domain is supplied.

## Remediation Guidance
- Avoid using predictable user inputs for redirection logic.
- Implement strict server-side validation against an allow-list of permitted domains or relative paths.
- Ensure any user input used for redirection is heavily sanitized and checked against valid application routes.
- Implement explicit interstitial pages warning users they are leaving the trusted domain.

## Report-Ready Writeup Template

```markdown
### [FINDING-ID] Open Redirect discovered on <endpoint / feature>

**Affected Component:** <endpoint / feature>
**Severity:** <medium / low>
**Confidence:** <0.0 – 1.0>

**Impact:**
An attacker can leverage this open redirect to facilitate phishing attacks, bypass SSRF protection, or steal OAuth tokens if used as a malicious callback URL. It degrades user trust in the application.

**Evidence:**
- <artifact path 1> — Shows the HTTP request navigating to the target and the server returning a 302 Redirect to an untrusted external domain.
- <artifact path 2> — Screenshot demonstrating the browser correctly following the redirect to the external site.

**Safe Reproduction Steps:**
1. Navigate to `<endpoint>?redirect_url=http://example.org`
2. Observe the HTTP Response headers contain `Location: http://example.org`
3. Notice that the browser automatically follows the redirect.

**Suggested Fix:**
Validate user-supplied URLs against a strict allowlist of trusted domains or relative paths. Reject or sanitize any unexpected input before executing the redirect.
```
