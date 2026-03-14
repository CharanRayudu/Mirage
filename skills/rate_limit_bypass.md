# Skill: Rate Limit Bypass

## Scope & Safety
- Allowed only if target is in `scope_lock.json` and ROE permits this class of testing.
- No destructive actions. No data exfiltration. No credential reuse outside test accounts.
- Avoid large-scale volumetric attacks (DoS/DDoS) that disrupt service. Only send the minimum number of requests (e.g., `< 50`) required to statistically prove the bypass exists.

## What to Collect (Evidence Checklist)
- Requests/responses (HAR or raw) capturing the full sequence of bypass attempts, importantly showing the response code changes (e.g., from `429 Too Many Requests` back to `200 OK`).
- The headers or parameters manipulated to trick the rate limit tracking mechanism (e.g., `X-Forwarded-For: 127.0.0.1`, `X-Originating-IP`).
- Timing statistics confirming requests were processed successfully far beyond the advertised rate threshold limit.

## Detection Heuristics
- Injecting IP-spoofing headers (e.g., `X-Forwarded-For`, `X-Real-IP`, `True-Client-IP`, `X-Remote-IP`) with a randomized value resets the rate limit counter.
- Changing casing or encoding in the URL path (e.g., `/api/v1/login` vs `/API/v1/login`) bypasses WAF or API Gateway tracking.
- Null-byte injection `%00` or trailing `/` bypasses strict URL metrics.
- Submitting an array of values `{"email":["userA@v.com","userB@v.com"]}` triggers simultaneous actions, bypassing iteration caps.

## Safe Test Procedure
1) Establish a baseline by intentionally triggering the API's rate limiting restriction (e.g., `HTTP 429 Too Many Requests`) on a safe endpoint like Password Reset or Login.
2) Replay the blocked HTTP request, append a spoofed header `X-Forwarded-For: 127.0.0.1`. If the response reverts to a `200 OK` or `401 Unauthorized`, the IP-based rate limit was bypassed.
3) Change the spoofed IP randomly (e.g., `127.0.0.2`) on every iteration to continuously bypass.
4) To check for casing bypasses, change a letter in the URL path and replay.
5) If suspicious, add a "Validator" task for safe confirmation, stopping immediately after verifying 5 consecutive successful requests.

## False-Positive Killers
- The `429 Too Many Requests` is thrown globally, irrespective of the IP, rendering header spoofing ineffective.
- The WAF drops the request (e.g., `HTTP 403 Forbidden`) upon inspecting invalid `X-Forwarded-For` syntax.
- The application parses the `X-Forwarded-For` header, but uses the originating TCP socket connection IP (e.g., Amazon API Gateway `remoteIp`) for accurate rate measurement.

## Remediation Guidance
- Utilize robust rate-limiting mechanisms that track authentication tokens (bearer tokens) or the verified physical TCP socket IP layer, rather than strictly relying on user-controllable application-layer HTTP headers.
- Sanitize and drop untrusted or spoofed IP headers if operating behind a trusted reverse proxy configuration or WAF. Use strongly authenticated `Forwarded` values.
- Enforce strict input validation against array-batching and null-bytes on API parameters to prevent horizontal scaling bypasses.

## Report-Ready Writeup Template

```markdown
### [FINDING-ID] Rate Limit Bypass via Header Spoofing on <endpoint / feature>

**Affected Component:** <endpoint / feature>
**Severity:** <high / medium>
**Confidence:** <0.0 – 1.0>

**Impact:**
Because the rate limit mechanism trusts unauthenticated application-layer headers such as `X-Forwarded-For`, an attacker can completely bypass throttling. This enables severe volumetric attacks like credential stuffing, OTP brute-forcing, application denial of service, or automated scraping at unbounded speeds.

**Evidence:**
- <artifact path 1> — Demonstrates the HTTP Request triggering the initial `429 Too Many Requests` block.
- <artifact path 2> — Showcases the subsequent HTTP request utilizing the injected `X-Forwarded-For: 1.2.3.4` payload effectively evading the block, returning `200 OK`.

**Safe Reproduction Steps:**
1. Send 5 continuous HTTP POST requests to `<endpoint>` to intentionally trigger the rate limiter.
2. Observe the server's initial `429 Too Many Requests` response.
3. Inject the header `X-Forwarded-For: [Random_IP]`.
4. Resend the request and observe the server successfully processes the action, entirely bypassing the defense.

**Suggested Fix:**
Disable blind trust in client-submitted `X-Forwarded-For` or `X-Real-IP` headers for rate calculation. Ensure the application configuration relies exclusively on the immediate upstream trusted proxy IP or validated application authentication tokens.
```
