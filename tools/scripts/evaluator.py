"""
evaluator.py — Frozen Harness for Objective Scoring.

This script parses the findings.db and events.jsonl to calculate an objective score 
for a given run_id. It operates strictly as a read-only scoring mechanism to 
prevent agents from changing the rules of the game mid-loop.
"""

import sqlite3
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class EvalScore:
    score: float
    new_valid_findings: int
    new_evidence_items: int
    coverage_delta: float
    risk_flags: list[str]


def count_new_evidence(events_jsonl: Path, run_id: str) -> int:
    """Read events.jsonl and count artifacts generated under this run_id."""
    if not events_jsonl.exists():
        return 0
    count: int = 0
    try:
        with events_jsonl.open("r", encoding="utf-8") as f:
            for line in f:
                evt = json.loads(line)
                if evt.get("type") == "NODE_END" and run_id in evt.get("stdout", ""):
                    # Count any node that successfully completed and produced artifacts
                    if evt.get("rc") == 0:
                        count += 1  # type: ignore
    except Exception:
        pass
    return count


def compute_risk_flags(events_jsonl: Path, run_id: str) -> list[str]:
    """Parse events to check if bbctl blocked commands or if tool timeouts occurred."""
    if not events_jsonl.exists():
        return []
        
    flags = []
    try:
        with events_jsonl.open("r", encoding="utf-8") as f:
            for line in f:
                evt = json.loads(line)
                if evt.get("type") == "NODE_END" and run_id in str(evt):
                    # Timeout rc code often -1
                    if evt.get("rc") == -1 and "timed out" in evt.get("stderr", ""):
                        flags.append("tool_timeout")
                    # If guardrails blocked it, we generally wouldn't get a NODE_END but just in case
                    if "BLOCKED" in evt.get("stderr", ""):
                        flags.append("scope_violation_attempt")
    except Exception:
        pass
        
    # Deduplicate flags
    return list(set(flags))


def evaluate_run(findings_db: Path, events_jsonl: Path, run_id: str, graph_path: Path | None = None) -> EvalScore:
    """Calculate the definitive multi-objective score for the run."""
    validated = 0
    
    # 1. Count findings
    if findings_db.exists():
        try:
            con = sqlite3.connect(findings_db)
            cur = con.cursor()
            
            # Create table if it doesn't exist just so we don't crash
            cur.execute('''
                CREATE TABLE IF NOT EXISTS findings (
                    id INTEGER PRIMARY KEY,
                    run_id TEXT,
                    status TEXT,
                    title TEXT,
                    evidence TEXT
                )
            ''')
            
            cur.execute("SELECT COUNT(*) FROM findings WHERE status='VALIDATED' AND run_id=?", (run_id,))
            row = cur.fetchone()
            if row:
                validated = row[0]
            con.close()
        except Exception as e:
            print(f"Error reading findings DB: {e}")

    # 2. Count new evidence generated
    new_evidence = count_new_evidence(events_jsonl, run_id)
    
    # 3. Simulate coverage delta (simplified for now as 1.0 per successful node)
    coverage_delta = float(new_evidence)
    
    # 4. Compute risk flags
    risk_flags = compute_risk_flags(events_jsonl, run_id)
    
    # Extract discovery stats if graph is provided
    discovery_bonus = 0.0
    if graph_path and graph_path.exists():
        try:
            graph = json.loads(graph_path.read_text(encoding="utf-8"))
            disc = graph.get("discoveries", {})
            discovery_bonus += len(disc.get("endpoints", [])) * 2.0
            discovery_bonus += len(disc.get("parameters", [])) * 1.0
            discovery_bonus += len(disc.get("vulnerabilities", [])) * 5.0
        except Exception:
            pass

    # 5. Calculate Score
    # Highly reward validated findings
    # Moderately reward coverage / evidence collection / discoveries
    # Heavily penalize risky behavior or out-of-scope probes
    score = (
        (10.0 * validated) +
        (1.0 * new_evidence) +
        (2.0 * coverage_delta) +
        discovery_bonus -
        (20.0 * (1.0 if "scope_violation_attempt" in risk_flags else 0.0)) -
        (5.0 * (1.0 if "tool_timeout" in risk_flags else 0.0))
    )
    
    return EvalScore(
        score=score,
        new_valid_findings=validated,
        new_evidence_items=new_evidence,
        coverage_delta=coverage_delta,
        risk_flags=risk_flags
    )
    
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run Evaluator")
    parser.add_argument("--program", help="Target program name")
    parser.add_argument("--run-id", help="Run ID for this execution")
    args = parser.parse_args()
    
    repo = Path(__file__).resolve().parents[2]
    
    if args.program and args.run_id:
        db_path = repo / "programs" / args.program / "findings.db"
        events_path = repo / "runs" / args.run_id / "events.jsonl"
        graph_path = repo / "runs" / args.run_id / "attack_graph.json"
        run_id = args.run_id
    else:
        # Fallback to positional arg for testing backwards-compatibility
        from sys import argv
        run_id = argv[1] if len(argv) > 1 else "target"
        db_path = repo / "state" / "findings.db"
        events_path = repo / "state" / "events.jsonl"
        graph_path = repo / "state" / "attack_graph.json"
        
    res = evaluate_run(db_path, events_path, run_id, graph_path)
    print(json.dumps(res.__dict__, indent=2))
