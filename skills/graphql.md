# Skill: GraphQL Security Testing

## Scope & Safety
- Allowed only if target is in `scope_lock.json`.
- No destructive mutations. Read-only queries for testing access controls.
- Never dump large datasets — query only enough to confirm behavior.

## Detection Heuristics
- Publicly reachable GraphQL endpoint(s) (`/graphql`, `/api/graphql`, `/gql`).
- Introspection enabled (schema queryable without auth).
- Overly permissive queries returning cross-tenant data.
- Missing rate limits / query complexity constraints.
- Batch query support (potential for abuse).
- Mutation operations accessible without proper authorization.

## Safe Test Procedure

1) **Identify GraphQL endpoint(s)** from traffic capture (HAR) or app config.
2) **Check introspection**:
   ```graphql
   { __schema { types { name } } }
   ```
   If enabled, document the full schema for analysis.
3) **Enumerate operations** via schema or documented API sources.
4) **For each operation that returns user/tenant objects:**
   - Verify it enforces tenant scoping with UserA vs UserB.
   - Check if filtering arguments can be bypassed.
5) **Test query depth/complexity:**
   - Try nested queries to check for depth limits.
   - Note any error messages about complexity limits.
6) **Record evidence** in HAR; never dump large datasets.

## Evidence Checklist
- [ ] GraphQL endpoint URL(s)
- [ ] Introspection result (enabled/disabled)
- [ ] Schema snapshot (if introspection enabled)
- [ ] HAR for cross-tenant query attempts
- [ ] Query complexity limit observations
- [ ] List of sensitive mutations accessible without auth

## False-Positive Killers
- Some introspection is intentional for development APIs.
- Public APIs may intentionally expose certain data.
- GraphQL subscriptions vs queries may have different auth rules.

## Remediation
- Disable introspection in production.
- Enforce authorization in resolvers (not just at the gateway).
- Add query depth/complexity limits and rate limits.
- Implement field-level authorization where needed.
- Log and monitor unusual query patterns.
