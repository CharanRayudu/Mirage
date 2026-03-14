"""
autoloop.py — Autonomous keep-or-revert experimentation loop.

This script manages the high-level Planner/Reflector iteration loop. It uses Git 
to save the state of `attack_graph.json`, executes the loop via bbctl.py, and uses
evaluator.py to score the run. If the plan failed or hit risk flags, it reverts 
the `attack_graph.json` state while safely leaving the forensic evidence in `artifacts/`.
"""

import json
import subprocess
import sys
import time
import argparse
from pathlib import Path

# Add script directory to sys.path so Pylance and Python can find evaluator.py
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from evaluator import evaluate_run  # type: ignore

REPO = SCRIPT_DIR.parent.parent

def git_is_clean(filepath: Path) -> bool:
    """Check if the specific file has uncommitted changes."""
    status = subprocess.run(["git", "status", "--porcelain", str(filepath)], capture_output=True, text=True)
    return status.stdout.strip() == ""


def git_commit(msg: str, filepath: Path) -> None:
    """Commit the specific file to git."""
    subprocess.check_call(["git", "add", str(filepath)])
    subprocess.check_call(["git", "commit", "-m", msg])


def git_reset_to(commit_sha: str, filepath: Path) -> None:
    """Reset the specific file back to the state at commit_sha."""
    # We use checkout to restore just the one file, dodging full branch resets.
    subprocess.check_call(["git", "checkout", commit_sha, "--", str(filepath)])
    # And commit the reversion so the working tree is clean
    subprocess.check_call(["git", "commit", "-m", f"Revert {filepath.name} to {commit_sha} (bad score)"])


def append_ledger_row(path: Path, row: dict) -> None:
    """Log the run experiment to the ledger (results.jsonl)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")


def run_bbctl_all(program: str, run_id: str) -> int:
    """Execute all pending nodes safely using the bbctl script."""
    bbctl = REPO / "tools" / "scripts" / "bbctl.py"
    cmd = [sys.executable, str(bbctl), "--run-all"]
    if program and run_id:
        cmd.extend(["--program", program, "--run-id", run_id])
    try:
        result = subprocess.run(
            cmd,
            cwd=str(REPO),
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        return result.returncode
    except Exception as e:
        print(f"Error running bbctl: {e}")
        return -1


def autoloop(program: str, run_id: str, iterations: int = 1) -> None:
    """Run the main testing loop X times."""
    
    if program and run_id:
        prog_dir = REPO / "programs" / program
        run_dir = REPO / "runs" / run_id
        ledger = prog_dir / "results.jsonl"
        graph_path = run_dir / "attack_graph.json"
        findings_db = prog_dir / "findings.db"
        events_jsonl = run_dir / "events.jsonl"
    else:
        state_dir = REPO / "state"
        ledger = state_dir / "results.jsonl"
        graph_path = state_dir / "attack_graph.json"
        findings_db = state_dir / "findings.db"
        events_jsonl = state_dir / "events.jsonl"
    
    if not graph_path.exists():
        print("✗ attack_graph.json missing.")
        return

    # Attempt to read current run_id
    try:
        graph = json.loads(graph_path.read_text(encoding="utf-8"))
        run_id = graph.get("run_id", "UNKNOWN_RUN")
    except Exception as e:
        print(f"Failed to read run_id: {e}")
        return

    # Ensure git is tracking the graph file
    try:
        subprocess.check_output(["git", "ls-files", "--error-unmatch", str(graph_path)])
    except subprocess.CalledProcessError:
        print(f"✗ {graph_path.name} is not tracked by git. Please git add and commit it first.")
        return

    # Get the baseline commit
    baseline_commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()
    print(f"Starting loop on baseline commit: {baseline_commit}")
    
    baseline_score: float = 0.0

    for i in range(iterations):
        print(f"\n[{i+1}/{iterations}] ═══ Iteration Start ═══")
        
        # 1. Provide an opportunity for Planner/LLM to Mutate the graph here.
        # In this implementation, we assume the Planner agent (Cursor/Antigravity) 
        # has ALREADY mutated `attack_graph.json` just before triggering this script,
        # OR will do it as part of a tool call in between loops.
        
        if git_is_clean(graph_path):
            print("  No changes to attack_graph.json detected. End of planner ideas.")
            break
            
        start_commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()
        git_commit(f"autoloop: plan iteration {i+1} for {run_id}", graph_path)
        current_commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()

        # 2. Execute
        rc = run_bbctl_all(program, run_id)

        # 3. Evaluate
        score = evaluate_run(findings_db, events_jsonl, run_id, graph_path)
        
        print(f"  Score: {score.score} | RC: {rc} | Flags: {score.risk_flags}")

        # 4. Keep or Revert Logic
        # Keep if execution didn't crash, score improved/maintained, and no scope violations
        keep = (rc == 0) and (score.score >= baseline_score) and ("scope_violation_attempt" not in score.risk_flags)
        status = "keep" if keep else "discard"

        # Log it
        append_ledger_row(ledger, {
            "ts": time.time(),
            "run_id": run_id,
            "iteration": i + 1,
            "commit": current_commit,
            "status": status,
            "score": score.score,
            "validated_findings": score.new_valid_findings,
            "coverage_delta": score.coverage_delta,
            "risk_flags": score.risk_flags
        })

        if keep:
            print(f"  ✓ KEEPING plan changes. New baseline score: {score.score}")
            baseline_score = max(baseline_score, score.score)
        else:
            print(f"  ✗ DISCARDING plan changes. Reverting to {start_commit}")
            git_reset_to(start_commit, graph_path)
            
        if "scope_violation_attempt" in score.risk_flags:
            print("  ! FATAL: Scope violation attempted. Halting autonomous loop.")
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous Iteration Loop")
    parser.add_argument("--program", help="Target program name", required=True)
    parser.add_argument("--run-id", help="Run ID for this execution", required=True)
    parser.add_argument("--iterations", type=int, default=1, help="Number of iterations")
    args = parser.parse_args()
    
    autoloop(args.program, args.run_id, args.iterations)
