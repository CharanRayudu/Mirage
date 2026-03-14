"""
bbctl.py — BugBounty Control: core task runner.

Executes the next eligible node from attack_graph.json after verifying scope
and command guardrails. Writes artifacts and appends to events.jsonl.

Usage:
    python tools/scripts/bbctl.py
    python tools/scripts/bbctl.py --run-all    # execute all runnable nodes in sequence
    python tools/scripts/bbctl.py --dry-run    # show what would run without executing
"""
import json
import os
import shlex
import subprocess
import sys
import time
import argparse
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


# ─── Helpers ───────────────────────────────────────────────────────────────────

def load_json(path: Path) -> dict:
    """Load a JSON file and return its contents."""
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict) -> None:
    """Write data to a JSON file (pretty-printed)."""
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def append_event(events_path: Path, evt: dict) -> None:
    """Append a JSON-line event to the audit trail."""
    with events_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(evt) + "\n")


# ─── Scope Checking ───────────────────────────────────────────────────────────

def is_target_allowed(scope: dict, target: str) -> bool:
    """Check if target URL is within the allowed scope prefixes."""
    prefixes = scope.get("allowed_targets", {}).get("url_prefixes", [])
    return any(target.startswith(p) for p in prefixes)


# ─── Command Guardrails ───────────────────────────────────────────────────────

DENY_PATTERNS = [
    "reverse shell", "nc -e", "bash -i", "powershell -enc",
    "rm -rf", ":(){:|:&};:", "curl | bash", "wget | sh",
    "mkfifo", "/dev/tcp", "python -c 'import socket",
    "eval(", "exec(", "os.system(",
]


def command_is_safe(cmd: list[str]) -> bool:
    """Check command against a deny-list of dangerous patterns."""
    joined = " ".join(cmd).lower()
    return not any(pattern in joined for pattern in DENY_PATTERNS)


# ─── Execution ─────────────────────────────────────────────────────────────────

def run_cmd(cmd: list[str], cwd: Path, timeout_s: int) -> tuple[int, str, str]:
    """Execute a command and return (returncode, stdout, stderr)."""
    try:
        result = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=timeout_s,
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", f"Command timed out after {timeout_s}s"
    except FileNotFoundError:
        return -1, "", f"Tool not found: {cmd[0]}"


def get_runnable_nodes(graph: dict) -> list[dict]:
    """Return nodes whose status is PENDING and all dependencies are DONE."""
    done = {n["id"] for n in graph["nodes"] if n["status"] == "DONE"}
    runnable = []
    for node in graph["nodes"]:
        if node["status"] != "PENDING":
            continue
        if all(dep in done for dep in node.get("depends_on", [])):
            runnable.append(node)
    return runnable


def execute_node(
    node: dict,
    graph: dict,
    graph_path: Path,
    events_path: Path,
    run_dir: Path,
    scope: dict,
    dry_run: bool = False,
) -> bool:
    """Execute a single node. Returns True on success."""
    run_id = graph["run_id"]
    cmd = [part.replace("<run_id>", run_id) for part in node["command_template"]]

    # ── Guardrail check ────────────────────────────────────────────────────
    if not command_is_safe(cmd):
        print(f"  ✗ BLOCKED by guardrails: {shlex.join(cmd)}")
        return False

    if dry_run:
        print(f"  [DRY-RUN] Would execute: {shlex.join(cmd)}")
        return True

    # ── Execute ────────────────────────────────────────────────────────────
    print(f"  ▶ Running: {shlex.join(cmd)}")
    append_event(events_path, {
        "ts": time.time(),
        "type": "NODE_START",
        "node_id": node["id"],
        "cmd": cmd,
    })

    timeout = int(
        scope.get("rate_limits", {})
        .get("tool_timeouts_seconds", {})
        .get("default", 300)
    )

    out_path = run_dir / f"{node['id']}.stdout.txt"
    err_path = run_dir / f"{node['id']}.stderr.txt"
    rc, out, err = run_cmd(cmd, cwd=REPO, timeout_s=timeout)

    out_path.write_text(out, encoding="utf-8")
    err_path.write_text(err, encoding="utf-8")

    # ── Normalize Output ───────────────────────────────────────────────────
    tool_name = node.get("tool")
    if tool_name and rc == 0:
        adapter_path = REPO / "tools" / "adapters" / f"parse_{tool_name}.py"
        if adapter_path.exists():
            norm_dir = run_dir.parent / "normalized"
            norm_dir.mkdir(parents=True, exist_ok=True)
            norm_path = norm_dir / f"{node['id']}_{tool_name}.json"
            try:
                adap_rc, adap_out, adap_err = run_cmd([sys.executable, str(adapter_path), str(out_path)], cwd=REPO, timeout_s=30)
                if adap_rc == 0:
                    norm_path.write_text(adap_out, encoding="utf-8")
                    node["artifacts"].append(str(norm_path))
                else:
                    print(f"  ! Adapter failed: {adap_err.strip()[:100]}")  # type: ignore
            except Exception as e:
                print(f"  ! Adapter error: {e}")

    # ── Update graph ───────────────────────────────────────────────────────
    node["status"] = "DONE" if rc == 0 else "FAILED"
    node["artifacts"].extend([str(out_path), str(err_path)])
    save_json(graph_path, graph)

    append_event(events_path, {
        "ts": time.time(),
        "type": "NODE_END",
        "node_id": node["id"],
        "rc": rc,
        "stdout": str(out_path),
        "stderr": str(err_path),
    })

    status_icon = "✓" if rc == 0 else "✗"
    print(f"  {status_icon} {node['id']} finished (rc={rc})")
    return rc == 0


# ─── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="BugBounty Control Runner")
    parser.add_argument("--program", help="Target program name")
    parser.add_argument("--run-id", help="Run ID for this execution")
    parser.add_argument("--dry-run", action="store_true", help="Dry run without executing")
    parser.add_argument("--run-all", action="store_true", help="Execute all runnable nodes")
    args = parser.parse_args()

    if args.program and args.run_id:
        prog_dir = REPO / "programs" / args.program
        run_dir_base = REPO / "runs" / args.run_id
        scope_path = run_dir_base / "scope_lock.yaml"
        graph_path = run_dir_base / "attack_graph.json"
        events_path = run_dir_base / "events.jsonl"
        run_dir = run_dir_base / "tool_outputs"
    else:
        # Fallback to legacy behavior
        scope_path = REPO / "scope" / "scope_lock.json"
        graph_path = REPO / "state" / "attack_graph.json"
        events_path = REPO / "state" / "events.jsonl"
        run_dir = None

    if not scope_path.exists():
        print(f"✗ Scope lock not found: {scope_path}")
        sys.exit(1)
    if not graph_path.exists():
        print(f"✗ attack_graph.json not found: {graph_path}")
        sys.exit(1)

    scope = load_json(scope_path)
    graph = load_json(graph_path)

    # ── Scope enforcement ──────────────────────────────────────────────────
    target = graph["target"]["value"]
    if not is_target_allowed(scope, target):
        print(f"✗ Target not allowed by scope config: {target}")
        sys.exit(1)

    run_id = graph.get("run_id", "default_run")
    if not run_dir:
        run_dir = REPO / "artifacts" / "runs" / run_id / "tool_outputs"
    run_dir.mkdir(parents=True, exist_ok=True)

    print(f"═══ bbctl ═══  run_id={run_id}  target={target}")
    print(f"  dry_run={args.dry_run}  run_all={args.run_all}\n")

    # ── Execution loop ─────────────────────────────────────────────────────
    while True:
        runnable = get_runnable_nodes(graph)
        if not runnable:
            print("\n  No runnable nodes remaining.")
            break

        node = runnable[0]
        print(f"─── Node: {node['id']} — {node['title']} ───")
        execute_node(node, graph, graph_path, events_path, run_dir, scope, args.dry_run)

        if not args.run_all:
            if len(runnable) > 1:
                print(f"\n  {len(runnable) - 1} more runnable node(s). Re-run to continue.")
            break

    print("\n═══ done ═══")


if __name__ == "__main__":
    main()
