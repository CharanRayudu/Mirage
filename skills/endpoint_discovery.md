# SKILL: Endpoint Discovery

## Goal
Discover HTTP endpoints across the target's attack surface using crawling, historical archives, and passive observation.

## Scope & Safety
- Only crawl in-scope domains at controlled concurrency and depth.
- Use passive sources (gau, waybackurls) before active crawling (katana).
- Respect robots.txt guidance where targets expect it.

## Tools
- **katana** — active web crawling with JSONL output and scope controls
- **gau** — fetch known URLs from Wayback Machine, Common Crawl, OTX, URLScan
- **waybackurls** — fetch archived URLs from the Wayback Machine
- **httpx** — validate discovered endpoints are alive

## Methodology
1. Run `gau <domain>` and `waybackurls <domain>` for historical endpoints.
2. Run `katana -u <url> -j -c 5 -p 2 -d 3` for active crawling with rate limits.
3. Deduplicate and validate with httpx.
4. Extract interesting patterns: API paths, admin panels, file uploads, auth endpoints.

## Output
- Deduplicated endpoint list with status codes and content types.
- Feed into `attack_graph.json` as `endpoint` nodes.

## Automation Hooks
- Emit `endpoint_discovered` for each new URL.
- Auto-categorize endpoints by pattern (API, auth, admin, static, upload).
