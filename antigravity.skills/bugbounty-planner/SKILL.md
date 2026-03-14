---
name: bugbounty-planner
description: Maintains attack_graph.json as a task DAG for safe, authorized security testing.
---

# BugBounty Planner Skill

## When Invoked

1. **Read** current state:
   - `scope/scope_lock.json` — what's allowed
   - `state/attack_graph.json` — current plan
   - `state/run_state.json` — memory notes from previous iterations
   - Latest artifacts in `artifacts/runs/<run_id>/`

2. **Analyze** the current state:
   - Which nodes are DONE? What did they find?
   - Which nodes FAILED? Why?
   - What evidence gaps exist?
   - What methodology skills apply? (check `skills/*.md`)

3. **Output** a minimal set of DAG edits:
   - `ADD_NODE` — new tasks with proper dependencies
   - `UPDATE_NODE` — status or description changes
   - `DEPRECATE_NODE` — mark dead-end tasks as SKIPPED

4. **Prioritize** 1–3 next tasks based on:
   - Cheap-first funnel (enumerate → probe → scan → validate → report)
   - Dependency readiness
   - Expected information gain

## Rules

- Every node MUST have: id, kind, title, description, tool, command_template, depends_on, status
- Use tools from `tools/tool_registry.yaml` only
- Never plan actions outside `scope_lock.json`
- Add `evidence_needed` annotation when a hypothesis lacks proof
- If a skill file doesn't exist for a test category, create one first
