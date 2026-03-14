---
name: bugbounty-executor
description: Executes attack_graph.json tasks safely using bbctl.py, capturing all artifacts and events.
---

# BugBounty Executor Skill

## When Invoked

1. **Read** the current plan:
   - `state/attack_graph.json` — find next runnable nodes
   - `scope/scope_lock.json` — verify target and action permissions

2. **Validate** before execution:
   - Target is in scope
   - Tool is in `tools/tool_registry.yaml`
   - Command passes guardrail checks (no deny-listed patterns)
   - Rate limits are respected

3. **Execute** using `tools/scripts/bbctl.py`:
   ```bash
   python tools/scripts/bbctl.py           # run next node
   python tools/scripts/bbctl.py --run-all  # run all runnable nodes
   python tools/scripts/bbctl.py --dry-run  # preview without executing
   ```

4. **Capture** all outputs:
   - stdout → `artifacts/runs/<run_id>/tool_outputs/<node_id>.stdout.txt`
   - stderr → `artifacts/runs/<run_id>/tool_outputs/<node_id>.stderr.txt`
   - Events → `state/events.jsonl` (NODE_START, NODE_END)

## Rules

- NEVER invent new tasks — only execute what the plan specifies
- NEVER broaden scope beyond `scope_lock.json`
- If a tool fails, capture stderr and stop — don't retry without Planner approval
- Always report: commands executed, artifact paths, errors, timing
