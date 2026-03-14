# Autoresearch as a Building Block for a Local-First BugBounty AI Agentic System

## Executive summary

The `karpathy/autoresearch` repository is **not** a security agent framework, but it is **highly relevant as a control-pattern** for building an elite, local-first BugBounty AI system—especially if you want **repeatable autonomous loops** with **tight scope**, **fixed evaluation**, and **keep-or-revert iteration**. Its core contribution is a minimal “autonomous experiment loop” encoded as a human-maintained instruction file (`program.md`) plus a strict split between a **read-only evaluator/environment** (`prepare.py`) and a **single mutable file** (`train.py`) that an agent is allowed to modify. citeturn7view1turn4view0turn5view2turn6view0

For a BugBounty AI agentic system (Planner‑Executor‑Reflector + multi-agent), the useful parts are therefore:

- **The “frozen harness + mutable state + objective scoring + reversible iteration” design** (excellent for safe, local-first, auditable autonomy). citeturn5view0turn5view2turn4view0  
- **The operational discipline encoded in `program.md`**: branch-per-run, redirect logs to avoid context flooding, parse key metrics via simple grep-able “key: value” output, and keep/discard via `git reset`. citeturn4view0turn6view0  
- **Experiment ledger + analysis tooling** (`results.tsv` + `analysis.ipynb`) which is directly adaptable to your `attack_graph.json` / `findings.db` / run metrics dashboards. citeturn4view0turn9view0

However, you should treat it as a **pattern library**, not a code library. Direct code reuse is limited because the repo is built around **ML training on a single NVIDIA GPU** and a specific metric (`val_bpb`), not security workflows. citeturn7view1turn5view0turn6view0

Also note governance risks: the README says “MIT,” but repo-level licensing is ambiguous because a LICENSE file may be missing (community raised this in an issue). citeturn7view3turn0search1

**Bottom line:** Use autoresearch to **shape your autonomous loop semantics**, your “read-only evaluator,” your “single-file mutable surface area,” and your “ledger + analysis” approach. Do **not** copy its “disable all permissions / LOOP FOREVER” stance into a BugBounty system; instead, replace with scope gates, legal ROE enforcement, and HITL escalation. citeturn7view1turn4view0

## What autoresearch is and what it contains

### Purpose and operating model

autoresesarch is presented as a minimal environment where an AI coding agent can run **time-boxed experiments** repeatedly: the agent changes code, runs a fixed-duration experiment, checks whether the metric improved, then keeps or discards the change—and repeats. citeturn7view1turn4view0

The README emphasizes that the repository is deliberately small and organized around **three key files**:

- `prepare.py`: fixed constants + data prep + evaluation utilities (not modified)  
- `train.py`: the single file the agent edits (model/optimizer/training loop)  
- `program.md`: instructions for the agent (“skill”) that the human edits over time citeturn7view1turn4view0

In `program.md`, the loop is explicitly specified (branch setup; only edit `train.py`; run `uv run train.py > run.log`; extract results; log to `results.tsv`; keep if improved else revert via git reset; repeat indefinitely). citeturn4view0

### “Frozen evaluator” and “fixed budget” mechanics

`prepare.py` contains fixed constants like `TIME_BUDGET = 300` seconds and a fixed evaluation function `evaluate_bpb` marked as “DO NOT CHANGE” to keep experiments comparable. citeturn5view0turn5view2

`train.py` enforces the time budget in the training loop and prints a deterministic summary at the end with parse-friendly lines such as `val_bpb: ...` and `peak_vram_mb: ...`. citeturn6view0turn6view1

### Tooling and dependencies

The README lists requirements including a single NVIDIA GPU (tested on H100), Python 3.10+, and the `uv` package manager; it supplies a quick start (`uv sync`, `uv run prepare.py`, `uv run train.py`). citeturn7view1

The `pyproject.toml` pins `torch==2.9.1` and configures an explicit `uv` index pointing at the CUDA 12.8 PyTorch wheel repository, alongside dependencies like `requests`, `pyarrow`, `pandas`, and `matplotlib`. citeturn10view0

### Maturity and repo surface area

As surfaced on the repository page at the time of retrieval, the repo shows ~31 commits, open issues and PRs, and no published releases. citeturn7view0turn7view4  
This strongly suggests “active early-stage” rather than a stable library intended for embedding.

## Concise assessment for BugBounty agentic systems

### Assessment table

| Dimension | What autoresearch provides | Usefulness for BugBounty AI | Notes |
|---|---|---|---|
| Primary purpose | Autonomous ML experimentation loop on single-GPU training, driven by an instruction “skill” file. citeturn7view1turn4view0 | Indirect but strong | You reuse **the loop discipline**, not the ML domain. |
| Core components | `program.md` (loop instructions), `prepare.py` (frozen harness), `train.py` (mutable file + time budget + summary output), `results.tsv` ledger + `analysis.ipynb`. citeturn7view1turn4view0turn5view0turn9view0 | High (as patterns) | Maps cleanly to “ROE/scope frozen + plan mutable + evidence ledger + analysis.” |
| License | README says “MIT.” citeturn7view3 | Caution | License file may be missing (community issue). Confirm before vendoring code. citeturn0search1 |
| Maturity | Small codebase; early iteration; no releases shown; active issues/PRs. citeturn7view0turn7view4 | Medium | Great for learning patterns; risky to treat as stable dependency. |
| Safety posture | Encourages “disable all permissions” and “LOOP FOREVER” autonomy in `program.md`. citeturn7view1turn4view0 | Needs heavy adaptation | For bug bounty, you must add ROE enforcement + HITL + stop conditions. |
| Supply-chain exposure | Downloads dataset from Hugging Face; uses `kernels` to load FlashAttention kernels from external repos at runtime. citeturn5view2turn6view1 | Important risk signal | Your BugBounty system should avoid runtime code downloads and use pinned tool binaries in containers. |

## Mapping autoresearch to Planner‑Executor‑Reflector and multi-agent architecture

The repo’s “loop” is conceptually P‑E‑R, but encoded as a single set of instructions rather than a multi-agent runtime. You can split it into your agents as follows.

### Component reuse map

```mermaid
flowchart LR
  subgraph Autoresearch
    PMD[program.md<br/>loop + rules]
    PRP[prepare.py<br/>frozen harness + evaluator]
    TRN[train.py<br/>mutable state + time budget]
    LED[results.tsv<br/>experiment ledger]
    LOG[run.log<br/>raw output]
    AN[analysis.ipynb<br/>metrics/plots]
    GIT[git keep/reset]
  end

  subgraph BugBounty System (Local-first)
    SCOPE[scope.yaml + ROE<br/>frozen rules]
    EVAL[evaluator.py<br/>safe scoring + policy checks]
    GRAPH[attack_graph.json<br/>mutable plan]
    FIND[(findings.db)]
    EVENTS[events.jsonl]
    ART[artifacts/<run_id>/...]
    REP[report + dashboards]
    CTRL[planner/executor/reflector<br/>orchestrator]
  end

  PMD --> CTRL
  PRP --> EVAL
  TRN --> GRAPH
  LED --> EVENTS
  LOG --> ART
  AN --> REP
  GIT --> CTRL
```

### Planner‑Executor‑Reflector mapping table

| Autoresearch element | P‑E‑R role analog | What to reuse | How to adapt for BugBounty |
|---|---|---|---|
| `program.md` loop steps (edit, run, parse, log, keep/reset) citeturn4view0 | Planner + Executor + Reflector combined | “Operating manual” format; strong constraints (“only change X”; “log outputs”; “avoid context flooding”). citeturn4view0 | Split into per-agent prompts and enforce scope/safety. Replace “NEVER STOP” with explicit stop conditions + HITL gates. citeturn4view0 |
| `prepare.py` constants + “DO NOT CHANGE” evaluator citeturn5view0turn5view2 | Frozen evaluator / policy spine | Hard separation of concerns: immutable evaluation and constants. | Your `scope.yaml`, ROE, evidence requirements, and scoring logic should be immutable during a run. |
| Fixed time budget (`TIME_BUDGET`) citeturn5view2turn6view0 | Execution constraints | Predictable iteration cadence; prevents runaway tasks. | Apply per-tool timeouts + per-target rate limits + max total run budget. |
| Summary output printed as `key: value` citeturn6view0 | Event emission | Extremely parseable telemetry. | Standardize tool wrappers to emit “finding_count: …” “new_evidence_items: …” etc (non-destructive). |
| `results.tsv` ledger + `analysis.ipynb` citeturn4view0turn9view0 | Memory + reporting | Simple ledger schema, post-run analytics, progress plots. | Replace TSV with JSONL + SQLite; keep a “run_progress notebook” or dashboard for coverage + validation metrics. |
| Git keep/reset strategy citeturn4view0 | Reversible planning | “Try an idea; keep if better; revert if not.” | Use git to version plan/prompt changes **only**, never to delete artifacts. Store evidence outside versioned tree or in gitignored folders. |

## Concrete integration plan for a BugBounty P‑E‑R system

The right integration strategy is to treat autoresearch as a **specimen of a great autonomy loop** and translate it into your repo’s orchestration layer, rather than importing ML code.

### Integration goals

1. **“Frozen harness” for security**: an immutable `scope.yaml` + `roe.md` + `evaluator.py` that define what is allowed, how you score progress, and what constitutes “valid evidence.” This mirrors the “DO NOT CHANGE” evaluator stance in `prepare.py`. citeturn5view0turn5view2  
2. **“Single mutable surface”**: constrain what the LLM may alter during a run to one of:
   - `attack_graph.json` (preferred), or
   - `skills/<skill>.md` (with explicit change review), or
   - `prompts/planner.md` (if you are doing prompt evolution).  
   This mirrors “single file to modify” in the README and `program.md`. citeturn7view1turn4view0  
3. **Keep-or-revert semantics**: after each iteration (or micro-batch of tasks), compute a score and either:
   - keep the plan changes, or
   - revert the mutable file to the previous commit.  
   This is explicitly described in the experiment loop. citeturn4view0

### Code-level “autoresesarch-style” control loop for bug bounty (safe, orchestration-only)

Below is pseudo-code (not exploit code) showing how to adapt “results.tsv + keep/revert” into your `attack_graph.json` and `findings.db` model.

```python
# tools/autoloop.py (pseudo-code)
from dataclasses import dataclass
import json, sqlite3, subprocess, time
from pathlib import Path

@dataclass
class EvalScore:
    score: float
    new_valid_findings: int
    new_evidence_items: int
    coverage_delta: float
    risk_flags: list[str]  # e.g., ["rate_limit_hit", "scope_near_boundary"]

def run_bbctl(run_id: str) -> int:
    # Executes next runnable nodes only (your safe executor).
    return subprocess.call(["python", "tools/scripts/bbctl.py"])

def evaluate_run(findings_db: Path, events_jsonl: Path) -> EvalScore:
    # Example: score favors VALIDATED findings + coverage, penalizes noise.
    con = sqlite3.connect(findings_db)
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM findings WHERE status='VALIDATED' AND run_id=?", (run_id,))
    validated = cur.fetchone()[0]
    # Parse events_jsonl for evidence/coverage metrics (your own schema).
    new_evidence = count_new_evidence(events_jsonl, run_id)
    coverage_delta = compute_coverage_delta(events_jsonl, run_id)
    risk_flags = compute_risk_flags(events_jsonl, run_id)

    # Multi-objective scoring: tune to avoid “optimize for BS findings”.
    score = (
        10.0 * validated +
        1.0 * new_evidence +
        5.0 * coverage_delta -
        20.0 * ("scope_violation_attempt" in risk_flags)
    )
    return EvalScore(score, validated, new_evidence, coverage_delta, risk_flags)

def git_commit(msg: str):
    subprocess.check_call(["git", "add", "state/attack_graph.json"])
    subprocess.check_call(["git", "commit", "-m", msg])

def git_reset_to(commit_sha: str):
    subprocess.check_call(["git", "reset", "--hard", commit_sha])

def append_ledger_row(path: Path, row: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")

def main():
    repo = Path(".")
    ledger = repo / "state" / "results.jsonl"
    run_id = json.loads((repo/"state/run_state.json").read_text())["run_id"]

    baseline_commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()
    baseline_score = None

    while True:  # replace "LOOP FOREVER" with stop conditions in your system
        start_commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()

        # 1) Planner proposes edits to attack_graph.json (human-reviewed if required)
        # 2) Commit the plan change (like autoresearch commits train.py)
        git_commit(f"plan: iteration for {run_id}")

        # 3) Execute
        rc = run_bbctl(run_id)

        # 4) Evaluate
        score = evaluate_run(repo/"state/findings.db", repo/"state/events.jsonl")

        if baseline_score is None:
            baseline_score = score.score

        keep = (rc == 0) and (score.score >= baseline_score) and ("scope_violation_attempt" not in score.risk_flags)
        status = "keep" if keep else "discard"

        append_ledger_row(ledger, {
            "ts": time.time(),
            "run_id": run_id,
            "commit": subprocess.check_output(["git","rev-parse","--short","HEAD"]).decode().strip(),
            "status": status,
            "score": score.score,
            "validated_findings": score.new_valid_findings,
            "coverage_delta": score.coverage_delta,
            "risk_flags": score.risk_flags
        })

        if keep:
            baseline_score = max(baseline_score, score.score)
        else:
            # Important: artifacts must not be lost; store them outside git-tracked paths or gitignore them.
            git_reset_to(start_commit)

        if stop_condition_met():
            break
```

This is the direct structural translation of `program.md`’s “commit → run → parse metrics → log → keep/reset” loop. citeturn4view0

### How to “wrap” autoresearch’s planner discipline into your Planner agent prompt

Your Planner prompt can borrow the *spirit* of `program.md` while changing the domain and safety rules. For example:

- Replace “only edit train.py” with “only edit attack_graph.json (and optionally one skill md).”
- Replace “val_bpb improved” with “score improved” where score is multi-objective and safety-penalized.
- Replace “NEVER STOP” with “stop if scope boundary risk or if time budget reached; require HITL for escalation.”

This is consistent with the structure and restrictions in `program.md` (single mutable file, no new deps, fixed evaluator, log discipline). citeturn4view0turn7view1

### Dockerization and IPC patterns

Autoresearch is designed to run on host GPU with local files and `uv`. citeturn7view1turn10view0  
For a BugBounty system, especially one that can run active scanners, a safer design is:

- Host process (Planner/Reflector; Cursor/Antigravity chat) writes and reads **only**:
  - `state/attack_graph.json`
  - `state/events.jsonl`
  - `state/findings.db`
- A containerized “Executor / tool-runner” receives tasks by **file-based IPC**:
  - It watches `attack_graph.json` for runnable nodes
  - Writes tool outputs under `artifacts/`
  - Appends immutable events to `events.jsonl`

This matches autoresearch’s log redirection pattern (“redirect everything; don’t flood context”) while giving you container isolation. citeturn4view0

## Recommended files and paths to inspect in autoresearch

Below is the minimal reading order that yields maximal architectural value.

| Path | Why it matters | What to read first |
|---|---|---|
| `README.md` | High-level spec: “3 files,” fixed 5-minute budget, `program.md` as a “skill,” quick start, license claim. citeturn7view1turn7view3 | Sections “How it works,” “Running the agent,” “Design choices,” “License.” citeturn7view1turn7view3 |
| `program.md` | The actual “agent operating system”: branch discipline, allowed/disallowed actions, loop semantics, log parsing, keep/discard rule, and “NEVER STOP” autonomy. citeturn4view0turn3view1 | “Setup,” “Experimentation,” “The experiment loop,” “Timeout/Crashes,” “NEVER STOP.” citeturn4view0turn3view1 |
| `prepare.py` | Shows how to encode a frozen evaluator and fixed constants; `TIME_BUDGET`; `evaluate_bpb` explicitly marked as fixed. citeturn5view0turn5view2 | Constants section (`TIME_BUDGET`) and evaluator section. citeturn5view0turn5view2 |
| `train.py` | Demonstrates budget enforcement + parse-friendly final summary output; also reveals supply-chain behavior around kernel loading. citeturn6view0turn6view1 | Import of `TIME_BUDGET`; budget loop break; “Final summary” prints. citeturn6view0turn6view1 |
| `analysis.ipynb` | Demonstrates a simple “ledger → analytics” pipeline; reads `results.tsv`, computes keep rate, plots progress. citeturn9view0 | Cells that parse TSV and compute keep/discard/crash counts; plot generation. citeturn9view0 |
| `pyproject.toml` | Reveals dependency constraints and `uv` CUDA wheel index configuration; informs reproducibility and supply-chain posture. citeturn10view0 | Dependencies list and `tool.uv.index` section. citeturn10view0 |
| `issues/38` (license) | Confirms potential mismatch: README says MIT but license file may not exist, affecting reuse strategy. citeturn0search1turn7view3 | Issue text and maintainer response (if any). citeturn0search1 |

## Risks and limitations for bug bounty use

### Key limitations

1. **Domain mismatch:** autoresearch is about ML training optimization, not security testing or tool orchestration; direct code reuse is minimal beyond orchestration patterns. citeturn7view1turn4view0  
2. **License ambiguity:** README claims MIT, but a missing LICENSE file (as flagged by community) creates legal uncertainty for code vendoring until clarified. citeturn7view3turn0search1  
3. **Unsafe autonomy defaults for security:** `program.md` explicitly encourages unbounded autonomy (“NEVER STOP”) and suggests disabling permissions, which is inappropriate for security tooling without ROE gates and escalation controls. citeturn7view1turn4view0  
4. **Supply chain exposure:**  
   - Data downloads from Hugging Face are hard-coded in `prepare.py` via `BASE_URL`. citeturn5view2  
   - `train.py` selects and loads flash-attention kernels via `get_kernel(repo)` pointing at external repositories based on GPU capability. citeturn6view1  
   For a bug bounty agent, you should avoid runtime code/module downloads and instead ship pinned tool images/binaries.

### Security-specific agent risks if you adopt the pattern

Even though autoresearch itself is not exploit code, its pattern (“agent edits code + runs shell commands in a loop”) can become dangerous in bug bounty contexts if not heavily constrained. `program.md` instructs the agent to use git operations and shell commands and to keep running indefinitely. citeturn4view0  
In a security system, that must be replaced with:

- strict allowlists of commands and targets  
- rate limiting  
- immutable ROE/scope enforcement  
- mandatory HITL on escalation categories  
- redaction of secrets in logs and reports

## Next steps and implementation checklist

### Recommended next steps

1. **Clone and audit** `karpathy/autoresearch` focusing on the “operating system” (`program.md`) and the “frozen evaluator” pattern (`prepare.py`). citeturn4view0turn5view0  
2. **Confirm licensing** before copying any code: reconcile README’s MIT statement with the presence/absence of a LICENSE file and any maintainer clarifications in issues. citeturn7view3turn0search1  
3. **Port the pattern** into your BugBounty repo:
   - Create `bb_program.md` as your agent “skill” (like `program.md`) but with security-safe constraints.
   - Implement a frozen `evaluator.py` (like `evaluate_bpb`) that produces a multi-objective score and forbids changing evaluation policy mid-run. citeturn5view0turn4view0  
4. **Use a ledger-first design**:
   - Replace `results.tsv` with `results.jsonl` + `findings.db`.
   - Keep git-tracked only: `attack_graph.json` + prompts/skills.
   - Keep artifacts outside git or gitignored, so `git reset --hard` never deletes evidence. citeturn4view0turn9view0  
5. **Containerize the executor** and use file-based IPC to mirror autoresearch’s log-redirection discipline while isolating tool execution. citeturn4view0

### Short implementation checklist

- [ ] `git clone https://github.com/karpathy/autoresearch`  
- [ ] Read `README.md`, `program.md`, `prepare.py`, `train.py`, `analysis.ipynb` in that order. citeturn7view1turn4view0turn5view0turn6view0turn9view0  
- [ ] Resolve license status (README vs LICENSE file; check issue #38). citeturn0search1turn7view3  
- [ ] In your BugBounty repo, implement:
  - [ ] `scope.yaml` + immutable ROE
  - [ ] `evaluator.py` (frozen) + multi-objective score
  - [ ] `attack_graph.json` as single mutable surface
  - [ ] `results.jsonl` ledger + `analysis.ipynb` dashboard (adapted from autoresearch’s notebook style) citeturn9view0  
- [ ] Add “keep/discard” logic with git commits for plan changes, never for artifacts. citeturn4view0  
- [ ] Add stop conditions + HITL escalation (replace “NEVER STOP”). citeturn4view0