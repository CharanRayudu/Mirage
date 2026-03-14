# Mirage

Local-first bug bounty workspace for planning, running, and reporting authorized security testing from a simple Python CLI.

Mirage is currently a lightweight scaffold around:

- per-program workspaces in `programs/`
- per-run artifacts in `runs/`
- a task graph in `attack_graph.json`
- a guarded task runner in `tools/scripts/bbctl.py`
- a keep-or-revert loop in `tools/scripts/autoloop.py`
- a SQLite findings store plus Markdown report generator

Use it only on targets you are explicitly authorized to test.

## What The Codebase Does Today

The current implementation provides these CLI commands from `mirage.py`:

- `program create <name>` creates a new program workspace under `programs/<name>/`
- `program list` lists available program folders
- `scan <program>` creates a run folder, copies the program graph and scope into it, and launches one `autoloop` iteration
- `recon <program>` currently follows the same run setup flow as `scan`
- `research <program>` prepares the research folder and prints instructions for using the web researcher agent to gather vulnerability intelligence
- `validate <program>` runs the 4-gate validation pipeline (Reproducibility, Scope Compliance, False Positive Elimination, Severity Estimation) on discovered findings
- `report <program>` reads `programs/<program>/findings.db` and writes a HackerOne-formatted Markdown report to `reports/<program>/`

Mirage is not a full autonomous platform yet. A number of parts are scaffolding or partially wired, so this README is intentionally implementation-first.

## Repository Layout

```text
Mirage/
  mirage.py
  mirage.bat
  agents/
  docker/
  programs/
  reports/
  runs/
  scope/
  skills/
  state/
  tools/
```

Important directories:

- `agents/` contains the prompt files for planner, executor, reflector, recon, auth, validation, reporting, and web research roles.
- `programs/` stores long-lived program state such as `program.yaml`, `scope.yaml`, `targets.txt`, `attack_graph.json`, and `findings.db`.
- `runs/` stores point-in-time execution artifacts for each scan or recon run.
- `tools/scripts/` contains the runtime pieces: DB init, runner, evaluator, autoloop, next tasks, and report generation.
- `tools/adapters/` contains parsers that normalize raw tool output into JSON (includes `subfinder`, `httpx`, `katana`, `gau`, `waybackurls`, `nuclei`, `ffuf`).
- `tools/tool_registry.yaml` describes supported tools, safety levels, and HITL expectations.
- `docker/` contains one compose file for a local lab and one for a sandbox/tool container setup.

## Requirements

Mirage itself is a Python script. The codebase directly depends on:

- Python 3.10+
- `PyYAML`
- Git

Optional external tools are described in `tools/tool_registry.yaml`, including `httpx`, `subfinder`, `katana`, `gau`, `waybackurls`, `nuclei`, `ffuf`, `nmap`, `sqlmap`, `zap`, `mitmproxy`, `burp`, and `playwright`.

## Quick Start

Create a program:

```bash
python mirage.py program create stripe
```

On Windows you can also use:

```bash
mirage.bat program create stripe
```

List programs:

```bash
python mirage.py program list
```

Start a run:

```bash
python mirage.py scan stripe
```

Run the research helper:

```bash
python mirage.py research stripe
```

Generate a report:

```bash
python mirage.py report stripe
```

Validate findings:

```bash
python mirage.py validate stripe
```

## Program Workspace

`program create <name>` creates this structure:

```text
programs/<name>/
  attack_graph.json
  findings.db
  notes.md
  program.yaml
  research/
  scope.yaml
  targets.txt
```

What gets seeded:

- `program.yaml` contains program metadata with placeholder values.
- `scope.yaml` contains `allowed_targets.url_prefixes` and default rate limits.
- `targets.txt` starts with `<name>.com`.
- `attack_graph.json` starts with a single pending `httpx` recon node.
- `findings.db` is initialized from `tools/scripts/init_db.py`.

## Run Flow

When you run `scan <program>` or `recon <program>`, `mirage.py` does the following:

1. Creates a dated run folder in `runs/`
2. Copies `scope.yaml` into the run as `scope_lock.yaml`
3. Copies the program `attack_graph.json` into the run and stamps the new `run_id`
4. Attempts to commit the seeded graph to Git
5. Launches one iteration of `tools/scripts/autoloop.py`

Run folders are expected to contain:

```text
runs/<run_id>/
  attack_graph.json
  events.jsonl
  logs/
  normalized/
  scope_lock.yaml
  tool_outputs/
```

`tools/scripts/bbctl.py` is the execution engine. It:

- reads the run graph and locked scope
- checks the target against allowed URL prefixes
- blocks commands matching deny-listed patterns
- executes runnable graph nodes
- writes stdout and stderr artifacts
- runs a matching parser from `tools/adapters/parse_<tool>.py` when available
- appends `NODE_START` and `NODE_END` events to `events.jsonl`

## Findings Database And Reports

The findings database schema lives in `tools/scripts/init_db.py`.

Main tables:

- `vulnerabilities`
- `evidence`
- `targets`
- `endpoints`
- `parameters`
- `tests`

`tools/scripts/reporter.py` generates reports from `vulnerabilities` and `evidence` and writes:

```text
reports/<program>/report_YYYY_MM_DD.md
```

## Safety Model

Mirage includes a few concrete guardrails in code:

- scope is defined per program in `programs/<program>/scope.yaml`
- commands are screened against a deny-list in `tools/scripts/bbctl.py`
- supported tools are cataloged in `tools/tool_registry.yaml`
- several tools are marked `requires_hitl: true`, including `ffuf`, `sqlmap`, `zap`, and `burp`
- some high-risk flags are explicitly denied, such as `nuclei -code` and `sqlmap --os-shell`

This project is for authorized testing only. The code and prompts do not make unauthorized use acceptable.

## Docker Helpers

The repo includes two optional compose files:

- `docker/docker-compose.lab.yml` starts local vulnerable labs on loopback, currently Juice Shop and DVGA.
- `docker/docker-compose.agent.yml` starts a simple sandbox container and an optional ProjectDiscovery tools container.

## Current Limitations

The codebase is still early-stage. A few things to know before relying on it:

- `research <program>` prints instructions for a human or agent workflow; it does not perform the research itself.
- `recon <program>` currently uses the same run bootstrap path as `scan <program>` and is not meaningfully different yet.
- the seed graph is minimal and starts with one `httpx` node.
- the tool registry is descriptive metadata; the runner does not yet enforce every policy declared there.
- the evaluator reads from a `findings` table for validated findings, while the DB initializer creates `vulnerabilities`, so parts of the scoring path are not aligned yet.
- there is active scaffolding in the repo, so expect rough edges and some unfinished integrations.

## License And Use

No explicit software license is included in this repository at the moment.

Use Mirage only for authorized security testing and lab work.
