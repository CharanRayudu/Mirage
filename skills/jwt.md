# Skill: JWT Validation & Session Integrity

## Scope & Safety
- Allowed only if target is in `scope_lock.json`.
- **Never attempt token forging** or signing with guessed keys.
- Focus on observing validation behavior, not bypassing it.

## Detection Heuristics
- JWT used as bearer token in `Authorization` header or cookies.
- Server accepts tokens across environments or unexpected audiences.
- Error messages suggest weak validation (e.g., "invalid signature" vs "token expired" reveals implementation details).
- Token payload contains sensitive data (PII, role info) without encryption.
- Long or missing expiry times.

## Safe Test Procedure

1) **Capture a legitimate login flow** and token issuance (HAR).
2) **Decode the JWT payload** (base64 only — this is public data):
   - Check `iss` (issuer), `aud` (audience), `exp` (expiry), `nbf` (not before)
   - Note claims: user ID, roles, permissions, tenant ID
3) **Verify server-side validation signals:**
   - **Expiry enforcement**: Use a known-expired token → should be rejected
   - **Audience enforcement**: Note if server checks `aud` claim
   - **Issuer enforcement**: Note if server checks `iss` claim
   - **Algorithm constraints**: Note the `alg` header value
4) **Check token lifecycle:**
   - How long until expiry?
   - Is there a refresh mechanism?
   - Does logout invalidate the token server-side?
5) **Document cookie/header security flags:**
   - `HttpOnly`, `Secure`, `SameSite` attributes
   - Token storage location (localStorage vs cookies)

## Evidence Checklist
- [ ] HAR of login flow showing token issuance
- [ ] Decoded JWT header and payload (redact signatures)
- [ ] Expiry enforcement test result (expired token → rejected?)
- [ ] Token lifetime observation
- [ ] Cookie/header security flags
- [ ] Logout invalidation behavior

## False-Positive Killers
- Some systems intentionally use long-lived tokens with server-side revocation lists.
- Audience/issuer may be validated at a different layer (API gateway).
- Development tokens may have different validation rules than production.

## Remediation
- Strict validation of `iss`, `aud`, `exp`, `nbf` claims.
- Use short-lived tokens with refresh mechanism.
- Key management hygiene: regular rotation, secure storage.
- Avoid storing sensitive data in token payload.
- Implement server-side token revocation for logout.
