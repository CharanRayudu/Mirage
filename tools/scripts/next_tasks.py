"""
next_tasks.py — Display the next runnable nodes from attack_graph.json.

Usage:
    python tools/scripts/next_tasks.py
    python tools/scripts/next_tasks.py --all   # show all nodes with statuses
"""
import json
import sys
import argparse
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def main() -> None:
    parser = argparse.ArgumentParser(description="Next Tasks Viewer")
    parser.add_argument("--program", help="Target program name")
    parser.add_argument("--run-id", help="Run ID for this execution")
    parser.add_argument("--all", action="store_true", help="Show all nodes")
    args = parser.parse_args()

    show_all = args.all
    if args.program and args.run_id:
        graph_path = REPO / "runs" / args.run_id / "attack_graph.json"
    else:
        graph_path = REPO / "state" / "attack_graph.json"

    if not graph_path.exists():
        print(f"✗ attack_graph.json not found at: {graph_path}")
        sys.exit(1)

    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    nodes = graph.get("nodes", [])
    done = {n["id"] for n in nodes if n["status"] == "DONE"}

    print(f"═══ Attack Graph: {graph['run_id']} ═══")
    print(f"  Target: {graph['target']['value']}")
    
    disc = graph.get("discoveries", {})
    endpoints = len(disc.get("endpoints", []))
    params = len(disc.get("parameters", []))
    vulns = len(disc.get("vulnerabilities", []))
    print(f"  Discoveries: {endpoints} endpoints | {params} parameters | {vulns} vulnerabilities")
    print(f"  Nodes:  {len(nodes)} total\n")

    if show_all:
        for node in nodes:
            icon = {"PENDING": "○", "DONE": "✓", "FAILED": "✗", "SKIPPED": "—"}.get(node["status"], "?")
            deps = ", ".join(node.get("depends_on", [])) or "none"
            print(f"  {icon} [{node['status']:8s}] {node['id']:6s} | {node['title']}")
            print(f"    {'':8s}  {'':6s}   tool={node.get('tool', 'N/A')}  deps=[{deps}]")
        print()

    # Show runnable nodes
    runnable = []
    for node in nodes:
        if node["status"] != "PENDING":
            continue
        if all(dep in done for dep in node.get("depends_on", [])):
            runnable.append(node)

    if runnable:
        print(f"  ▶ Runnable now ({len(runnable)}):")
        for node in runnable:
            print(f"    • {node['id']} — {node['title']} (tool: {node.get('tool', 'N/A')})")
    else:
        print("  No runnable nodes.")

    # Summary stats
    pending = sum(1 for n in nodes if n["status"] == "PENDING")
    done_count = len(done)
    failed = sum(1 for n in nodes if n["status"] == "FAILED")
    print(f"\n  Stats: {done_count} done, {pending} pending, {failed} failed")


if __name__ == "__main__":
    main()
