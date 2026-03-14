---
name: bugbounty-reflector
description: Validates evidence, updates hypotheses, detects loops, and writes memory notes for the P-E-R cycle.
---

# BugBounty Reflector Skill

## When Invoked

1. **Read** execution results:
   - Latest artifacts in `artifacts/runs/<run_id>/tool_outputs/`
   - `state/events.jsonl` — recent NODE_END events
   - `state/attack_graph.json` — current plan state
   - `state/run_state.json` — previous memory notes

2. **Analyze** artifacts:
   - Parse tool outputs using adapters in `tools/adapters/`
   - Separate confirmed evidence from noise
   - Identify candidate findings

3. **Classify** results:
   - **Confirmed** — evidence + reproduction path exists
   - **Hypothesis** — suspicious but needs more data (assign confidence 0.0–1.0)
   - **False Positive** — evidence contradicts the claim
   - **Dead End** — tested and nothing found

4. **Update** state:
   - Propose DAG edits: add evidence-gathering tasks, prune loops, deprecate dead ends
   - Write memory notes to `state/run_state.json`: patterns, quirks, insights
   - If a node has failed 3+ times, recommend marking it SKIPPED

5. **Output** structured report:
   - "What We Know" — evidence-backed facts
   - "What We Suspect" — ranked hypotheses
   - "What To Do Next" — proposed plan edits
   - "Memory Notes" — persistent learnings

## Rules

- Never promote a hypothesis to finding without evidence
- Always cite artifact paths when making claims
- Detect loops: same node failing repeatedly, similar tasks being added
- Update `run_state.json` with patterns for future iterations
