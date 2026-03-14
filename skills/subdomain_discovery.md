# SKILL: Subdomain Discovery

## Goal
Enumerate subdomains of in-scope root domains to expand the attack surface using passive and active DNS techniques.

## Scope & Safety
- Only enumerate subdomains under root domains listed in `programs/<program>/scope.yaml`.
- Use passive sources first (subfinder, crt.sh, DNS); active brute-force only with HITL.
- Respect rate limits on DNS resolvers.

## Tools
- **subfinder** — passive subdomain enumeration via APIs (Shodan, Censys, VirusTotal, etc.)
- **dnsx** — DNS resolution and validation
- **amass** — comprehensive attack surface mapping (passive mode)

## Methodology
1. Run `subfinder -d <domain> -oJ` to collect subdomains from passive sources.
2. Pipe results through `dnsx` to validate DNS resolution.
3. Feed live subdomains into httpx for HTTP probing.
4. Store results in `programs/<program>/tool_outputs/subfinder.jsonl`.

## Output
- List of validated subdomains with DNS resolution status.
- Feed into `attack_graph.json` as `subdomain` nodes linked to `host` parent.

## Automation Hooks
- Emit `subdomain_discovered` events to attack graph.
- Auto-trigger httpx probing for newly discovered subdomains.
