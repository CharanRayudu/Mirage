# SKILL: A06 Insecure Design (OWASP Top 10:2025)

## Goal
Find design-level security gaps via workflow abuse-case analysis in a black-box setting.

## Scope & Safety
- This skill is inherently context-heavy: require HITL for conclusions.
- Keep tests low-volume; avoid stressing business workflows.

## Granular Skills
- `business_logic.md`, `rate_limit_bypass.md`, `auth_testing.md`

## Detection Heuristics
- Missing step-up auth for sensitive operations.
- Missing rate limits on high-value endpoints.
- Broken state machines (skip steps, reuse tokens).
- "Trust the client" behaviors (prices, roles, flags in request body).

## Safe Test Steps
1. Map critical workflows (signup, login, reset, payments, role changes).
2. Use Playwright to record deterministic, repeatable flows.
3. Try safe invariants: replay earlier step tokens in later steps, omit required steps and observe server acceptance.
4. Document expected security properties and observed gaps.

## Evidence
- Workflow diagram + replayable runbook.
- Clear preconditions (account types, roles), and observed behavior.

## Automation Hooks
- Emit `workflow_mapped`, `invariant_tested`, `finding_candidate`.
