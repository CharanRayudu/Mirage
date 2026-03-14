# Skill: Authentication & Authorization Testing

## Scope & Safety
- Allowed only if target is in `scope_lock.json` and ROE permits authenticated testing.
- Use only designated test accounts. Never use production credentials.
- Do not test logout or irreversible routes unless explicitly requested.

## What to Verify

### Session Lifecycle
- Login mechanism (credentials, OAuth, SSO, MFA)
- Token/session issuance and storage
- Session duration and refresh behavior
- Logout and invalidation

### MFA/TOTP Handling
- Is MFA enforced for all users or only some roles?
- Can MFA be bypassed by replaying old codes?
- Rate limiting on MFA attempts

### Access Control Boundaries
- Role-based access (admin vs user vs guest)
- Tenant isolation (cross-tenant data access)
- Feature gating (premium vs free tier)
- API vs UI access control consistency

## Safe Test Procedure

1) **Capture login flow and post-login navigation (HAR):**
   - Document the authentication mechanism
   - Note token types (JWT, session cookie, API key)
   - Record all security-relevant headers

2) **Verify session properties:**
   - Cookie flags: `HttpOnly`, `Secure`, `SameSite`, `Domain`, `Path`
   - Token storage location: cookie vs localStorage vs sessionStorage
   - Session fixation: does session ID change after login?
   - Concurrent sessions: are multiple sessions allowed?

3) **Check revocation behavior:**
   - Does logout invalidate the server-side session?
   - Can expired tokens still be used?
   - Password change → are existing sessions invalidated?

4) **Test auth boundaries (two-account method):**
   - Access profile/settings endpoints with UserA's token as UserB
   - Access admin endpoints with non-admin token
   - Access billing/payment endpoints with restricted-role token

5) **Encode login flow steps explicitly** for reproducible automation:
   ```json
   {
     "login_flow": [
       {"step": "navigate", "url": "/login"},
       {"step": "fill", "selector": "#email", "value": "{{TEST_USER}}"},
       {"step": "fill", "selector": "#password", "value": "{{TEST_PASS}}"},
       {"step": "click", "selector": "#submit"},
       {"step": "wait", "condition": "url_contains", "value": "/dashboard"}
     ]
   }
   ```

## Evidence Checklist
- [ ] HAR of complete login flow
- [ ] Token/session properties documented
- [ ] Cookie security flags documented
- [ ] Session fixation test result
- [ ] Logout invalidation test result
- [ ] Cross-role access test results (with HAR)
- [ ] Cross-tenant access test results (with HAR)
- [ ] MFA enforcement observations

## Remediation
- Enforce authentication on all protected endpoints (server-side).
- Use short-lived tokens with server-side revocation.
- Set proper cookie flags: `HttpOnly`, `Secure`, `SameSite=Strict`.
- Regenerate session IDs after login.
- Enforce MFA for sensitive operations.
- Rate-limit authentication attempts.
- Log and alert on suspicious auth patterns.
