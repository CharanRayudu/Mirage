# SKILL: API Discovery

## Goal
Discover REST, GraphQL, and other API surfaces exposed by target applications.

## Scope & Safety
- Only probe in-scope domains.
- Use passive discovery and safe GET/OPTIONS/HEAD requests.
- Do not send mutation queries to GraphQL without HITL.

## Methodology
1. **OpenAPI/Swagger detection** — Probe common paths: `/swagger.json`, `/openapi.json`, `/api-docs`, `/v1/docs`, `/v2/api-docs`.
2. **GraphQL detection** — Probe `/graphql`, `/gql`, `/api/graphql` with safe introspection query.
3. **REST API enumeration** — Use katana + gau output to identify `/api/v*` patterns.
4. **WSDL/SOAP detection** — Probe `?wsdl` suffix on discovered service endpoints.
5. **Documentation scraping** — Check for Redoc, Stoplight, or custom API portals.

## Detection Heuristics
- JSON responses from undocumented endpoints
- GraphQL introspection enabled (information disclosure)
- API versioning patterns revealing old/deprecated versions
- CORS headers indicating API usage

## Output
- API inventory with type (REST/GraphQL/SOAP), version, authentication requirements.
- Feed into `attack_graph.json` as `service` nodes.

## Automation Hooks
- Emit `api_discovered`, `graphql_introspection_found`, `api_version_detected`.
