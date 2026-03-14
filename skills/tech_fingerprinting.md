# SKILL: Technology Fingerprinting

## Goal
Identify the technology stack (web servers, frameworks, languages, CDNs, WAFs) of target applications using externally observable signals.

## Scope & Safety
- Passive fingerprinting only (response headers, HTML meta, JS libraries).
- No intrusive version checks. Use what the server voluntarily discloses.

## Methodology
1. **HTTP Headers** — Analyze `Server`, `X-Powered-By`, `X-AspNet-Version`, `X-Generator` headers.
2. **HTML Meta Tags** — Check `<meta name="generator">`, framework-specific class names, CSS patterns.
3. **JavaScript Libraries** — Detect React, Angular, Vue, jQuery versions from bundle patterns or global variables.
4. **Cookie Patterns** — Framework-specific session cookie names (PHPSESSID, JSESSIONID, connect.sid).
5. **Error Pages** — Default error pages reveal server/framework identity.
6. **SSL/TLS Certificates** — Issuer patterns may indicate CDN/WAF (Cloudflare, Akamai).

## Detection Heuristics
- Known header patterns for nginx, Apache, IIS, Express, Django, Rails, Spring.
- WAF signatures in response headers or blocked request behaviors.
- CDN indicators (cf-ray, x-amz-cf-id, akamai-cache-status).

## Output
- Technology profile with confidence levels per signal.
- Feed into `attack_graph.json` as `technology` nodes linked to hosts/services.
- Cross-reference with A03 (supply chain) for CVE correlation.

## Automation Hooks
- Emit `technology_fingerprinted`, `waf_detected`, `cdn_detected`.
