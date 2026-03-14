# Skill: OAuth Misconfiguration

## Scope & Safety
- Allowed only if target is in `scope_lock.json` and ROE permits this class of testing.
- No destructive actions. No data exfiltration. No credential reuse outside test accounts.
- Test workflows exclusively using the authorized accounts configured for the system. Do not steal or hijack tokens belonging to unrelated production users.

## What to Collect (Evidence Checklist)
- Requests/responses (HAR or raw) capturing the full OAuth authorization flow (Authorization Request, Callback).
- The `redirect_uri` parameter used during the flow and any server response reflecting it.
- Tokens or code fragments exposed in HTTP referers or URL parameters.
- Presence (or absence) of the `state` or `nonce` parameters.

## Detection Heuristics
- Modifying the `redirect_uri` to an external website successfully forwards the OAuth Authorization Code or Implicit Token to the external attacker site.
- The `state` parameter is either missing, ignored, or not cryptographically tied to the user's session, enabling CSRF.
- The application trusts the Authorization Code exchanged without validating the callback URL strictness on the backend.
- Flaws in Implicit flows where Access Tokens are leaked in the URL fragment.

## Safe Test Procedure
1) Establish a baseline legitimate OAuth login flow utilizing the two authorized test accounts (Account A and Account B).
2) To test Open Redirects in `redirect_uri`: During the authorization redirect, manipulate the `redirect_uri` parameter to an external domain (e.g., `https://evil.org`). Analyze if the IDP accepts and redirects the code to it.
3) To test CSRF (Missing State): Capture Account A's valid authorization callback URL (e.g., `?code=VALID_CODE`). Drop the request. In a fresh session (Account B), navigate directly to that callback URL to see if Account B is forcefully authenticated as Account A.
4) If suspicious, add a "Validator" task for safe confirmation.

## False-Positive Killers
- The modified `redirect_uri` fails validation at the Identity Provider (IDP) returning an error.
- The `state` parameter omission causes a server-side rejection (HTTP 400).
- Cross-Site Request Forgery via OAuth injection fails because the code is expired or explicitly bound to a PKCE challenge.

## Remediation Guidance
- Enforce strict, exact-match validation of `redirect_uri` configurations at the IDP level. Never rely on partial matching or regex-based domains.
- Implement the `state` parameter securely to bind the authentication flow uniquely to the user's initiating browser session.
- Favor the Authorization Code Flow with PKCE over Implicit Flows to mitigate token exposure vulnerabilities in the client runtime.
- Do not transmit Access Tokens via URL parameters or fragments to third-party referrers.

## Report-Ready Writeup Template

```markdown
### [FINDING-ID] OAuth Authorization Flaw on <endpoint / feature>

**Affected Component:** <endpoint / feature>
**Severity:** <high / medium>
**Confidence:** <0.0 – 1.0>

**Impact:**
Because of weak OAuth parameter validation, an attacker could either hijack another user's authentication credentials (via redirect_uri tampering) or force a victim to log into an attacker-controlled account (via CSRF/missing state), severely breaking account confidentiality and integrity.

**Evidence:**
- <artifact path 1> — Demonstrates the modified OAuth authorization request.
- <artifact path 2> — Showcases the vulnerable server response correctly responding to the hijacked callback or successfully executing the injected CSRF.

**Safe Reproduction Steps:**
1. Intercept the standard OAuth authorization redirect intended for the IDP.
2. Manipulate the security parameter (e.g., remove `state`, or alter `redirect_uri`).
3. Complete the login flow and observe that the application fails to validate the manipulated variable securely.

**Suggested Fix:**
Enforce strict `redirect_uri` validation using exact string matching on the Authorization Server. Require and validate a cryptographically secure `state` parameter to defeat CSRF. Follow modern OAuth 2.0 BCPs, heavily preferencing PKCE deployments.
```
