# Skill: XSS (Detection + Safe Validation Structure)

## Scope & Safety
- Allowed only if target is in `scope_lock.json`.
- Use only non-executable marker strings for reflection detection.
- No data access, no persistence, no phishing payloads.
- For confirmed XSS, validate only in local lab / staging with program-approved proof.

## Detection Heuristics
- Unescaped reflection of user input in HTML/JS contexts.
- Stored display of user-generated content without encoding.
- Dynamic rendering of URL parameters into page content.
- Client-side template injection points (Angular, Vue, React dangerouslySetInnerHTML).
- Missing/weak Content-Security-Policy headers.

## Safe Test Procedure

1) **Identify input reflection points:**
   - Use a unique, non-executable marker string (e.g., `MIRAGE_XSS_PROBE_12345`).
   - Submit it via each input vector (query params, form fields, headers, cookies).
   - Search for the marker in the response body.

2) **Determine context** where marker appears:
   - HTML body: `<p>MIRAGE_XSS_PROBE_12345</p>`
   - HTML attribute: `<input value="MIRAGE_XSS_PROBE_12345">`
   - JavaScript: `var x = "MIRAGE_XSS_PROBE_12345";`
   - URL: `<a href="MIRAGE_XSS_PROBE_12345">`
   - CSS: `background: url(MIRAGE_XSS_PROBE_12345)`

3) **Check encoding behavior:**
   - Submit HTML special chars: `< > " ' & /`
   - Observe which are encoded vs. reflected raw.
   - Document the encoding (or lack thereof) for each context.

4) **If reflection is unescaped**, create Validator task:
   - Validate in a local lab / staging first.
   - Use only non-destructive, program-approved proof.
   - No data access, no persistence, no phishing.

5) **Capture evidence:**
   - Screenshot of DOM showing unescaped reflection.
   - HAR of the request/response pair.
   - Note the exact context and input vector.

## Evidence Checklist
- [ ] Marker string used
- [ ] Input vector(s) tested (query, form, header, etc.)
- [ ] Reflection point(s) found with context type
- [ ] Encoding behavior for special characters
- [ ] Screenshot showing unescaped reflection in DOM
- [ ] HAR of request/response
- [ ] CSP header analysis

## False-Positive Killers
- WAF/CDN stripping or encoding input
- Client-side framework auto-escaping (React, Angular default behavior)
- Browser XSS auditors (though deprecated in modern browsers)
- Response content type preventing rendering (e.g., `application/json`)

## Remediation
- Context-aware output encoding (HTML, JS, URL, CSS contexts need different encoding).
- Content-Security-Policy (CSP) with strict directives.
- Trusted Types API where applicable.
- Input validation (allowlist, not denylist).
- HttpOnly flag on session cookies to limit impact.
