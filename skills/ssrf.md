# Skill: SSRF (Heuristic + Evidence-Driven Confirmation)

## Scope & Safety
- Allowed only if target is in `scope_lock.json`.
- **Do NOT probe internal metadata endpoints** (e.g., `169.254.169.254`) unless explicitly permitted in ROE.
- Use only controlled canary endpoints you own.

## Detection Heuristics
- Server fetches user-supplied URLs (webhooks, image fetchers, link previews, importers, PDF generators).
- Error messages indicate outbound fetch attempts (connection timeouts, DNS resolution errors).
- URL parameters that accept full URLs or hostnames.
- Features that render remote content (iframe sources, embeds, imports).

## Safe Test Procedure

1) **Identify URL-fetch features** and capture baseline behavior:
   - Webhook configuration pages
   - Image/avatar upload-by-URL
   - Link preview generators
   - Document importers (PDF, CSV from URL)
   - API integrations that fetch external data

2) **Use a controlled canary endpoint:**
   - Use a DNS/HTTP callback service you control (e.g., Burp Collaborator, interactsh).
   - Or use a simple HTTP server you run locally.
   - Submit the canary URL through each identified feature.

3) **Confirm outbound request:**
   - Check if your canary received a request.
   - Capture the request details (source IP, headers, timing).

4) **Check constraints (if canary hit):**
   - Test allowed schemes: `http://`, `https://`, `file://`, `gopher://`
   - Test allowed ports: standard vs. non-standard
   - Check for DNS rebinding protections
   - Check for IP range blocks (private IP rejection)

5) **Do NOT probe internal services** unless ROE explicitly permits it.

## Evidence Checklist
- [ ] URL-fetch feature identified with endpoint details
- [ ] Canary URL submitted and request captured
- [ ] Source IP and headers from canary callback
- [ ] Scheme restriction test results
- [ ] Port restriction test results
- [ ] IP range block test results
- [ ] HAR of the triggering request

## False-Positive Killers
- Some URL-fetch features use server-side proxies that are intentional (e.g., image CDN resizing).
- WAF/proxy may intercept and rewrite URLs.
- DNS-level filtering may block resolution but not the SSRF itself.
- Rate limiting may prevent consistent reproduction.

## Remediation
- Strict allowlist of permitted domains/IPs.
- Egress proxy for all outbound requests.
- DNS pinning to prevent rebinding attacks.
- Block private/reserved IP ranges (RFC 1918, link-local, loopback).
- Disable unnecessary URL schemes (only `http`/`https`).
- Request sanitization and validation.
- Monitor and log all outbound requests from URL-fetch features.
