#!/usr/bin/env python3
"""
mirage.py — Main CLI entrypoint for the Mirage Bug Bounty AI System

Usage:
  mirage program create <name>
  mirage program list
  mirage scan <program>
  mirage recon <program>
  mirage research <program>
  mirage validate <program>
  mirage report <program>
"""

import argparse
import sys
import os
import time
import shutil
import subprocess
import json
from pathlib import Path
import yaml  # type: ignore

REPO = Path(__file__).resolve().parent

def ensure_dirs():
    (REPO / "programs").mkdir(exist_ok=True)
    (REPO / "runs").mkdir(exist_ok=True)
    (REPO / "reports").mkdir(exist_ok=True)

def cmd_program_create(args):
    name = args.name
    prog_dir = REPO / "programs" / name
    if prog_dir.exists():
        print(f"✗ Program '{name}' already exists.")
        sys.exit(1)
        
    prog_dir.mkdir(parents=True)
    
    # Create program.yaml
    program_yaml = {
        "program_name": name,
        "platform": "private",
        "program_url": "https://example.com/bounty",
        "notes": f"Initial setup for {name}"
    }
    with (prog_dir / "program.yaml").open("w") as f:
        yaml.dump(program_yaml, f, sort_keys=False)
        
    # Create scope.yaml
    scope_yaml = {
        "allowed_targets": {
            "url_prefixes": [
                f"https://*.{name}.com"
            ]
        },
        "rate_limits": {
            "requests_per_second": 2,
            "tool_timeouts_seconds": {
                "default": 300
            }
        }
    }
    with (prog_dir / "scope.yaml").open("w") as f:
        yaml.dump(scope_yaml, f, sort_keys=False)
        
    # Create targets.txt
    (prog_dir / "targets.txt").write_text(f"{name}.com\n", encoding="utf-8")
    
    # Create notes.md
    (prog_dir / "notes.md").write_text(f"# Notes for {name}\n", encoding="utf-8")
    
    # Create attack_graph.json (v2 schema with expanded discovery categories)
    attack_graph = {
        "run_id": "template",
        "target": {
            "type": "url",
            "value": f"https://{name}.com"
        },
        "discoveries": {
            "hosts": [],
            "subdomains": [],
            "services": [],
            "endpoints": [],
            "parameters": [],
            "auth_contexts": [],
            "technologies": [],
            "vulnerability_candidates": [],
            "validated_findings": [],
            "vulnerabilities": []
        },
        "nodes": [
            {
                "id": "n1",
                "kind": "recon",
                "status": "PENDING",
                "title": "Probe HTTP surface",
                "description": "Initial active probing of discovered endpoints.",
                "tool": "httpx",
                "command_template": [
                    "httpx", "-silent", "-probe", "-list",
                    "runs/<run_id>/inputs/hosts.txt"
                ],
                "depends_on": [],
                "artifacts": [],
                "owasp_tags": []
            }
        ],
        "edges": [],
        "edge_types": ["hosts", "exposes", "uses", "accepts", "suggests", "validates"],
        "policies": {
            "no_exploitation": True,
            "require_hitl_for_active_fuzzing": True
        }
    }
    with (prog_dir / "attack_graph.json").open("w", encoding="utf-8") as f:
        json.dump(attack_graph, f, indent=2)
    
    # Create research directory
    (prog_dir / "research").mkdir(exist_ok=True)
    
    # Initialize findings DB
    init_db_script = REPO / "tools" / "scripts" / "init_db.py"
    subprocess.run([sys.executable, str(init_db_script), name], cwd=REPO)
    
    print(f"✓ Created program '{name}' in programs/{name}")

def cmd_program_list(args):
    prog_dir = REPO / "programs"
    if not prog_dir.exists():
        print("No programs found.")
        return
        
    programs = [d.name for d in prog_dir.iterdir() if d.is_dir()]
    if not programs:
        print("No programs found.")
        return
        
    print("Programs:")
    for p in programs:
        print(f"  - {p}")

def generate_run_id(program):
    date_str = time.strftime("%Y_%m_%d")
    return f"run_{date_str}_{program}"

def initiate_scan(program, is_recon_only=False):
    prog_dir = REPO / "programs" / program
    if not prog_dir.exists():
        print(f"✗ Program '{program}' does not exist.")
        sys.exit(1)
        
    run_id = generate_run_id(program)
    # Check if run ID already exists for today (append counter if needed, simplified for now)
    run_dir = REPO / "runs" / run_id
    counter = 1
    while run_dir.exists():
        run_id = f"{generate_run_id(program)}_{counter}"
        run_dir = REPO / "runs" / run_id
        counter += 1
        
    run_dir.mkdir(parents=True)
    (run_dir / "logs").mkdir(exist_ok=True)
    (run_dir / "tool_outputs").mkdir(exist_ok=True)
    
    print(f"▶ Starting scan for '{program}' (Run ID: {run_id})")
    print(f"  Outputs will be saved to: {run_dir.relative_to(REPO)}")
    
    # Lock scope for this run
    shutil.copy2(prog_dir / "scope.yaml", run_dir / "scope_lock.yaml")
    
    # Seed the attack graph for this run
    graph_path = run_dir / "attack_graph.json"
    shutil.copy2(prog_dir / "attack_graph.json", graph_path)
    
    # Update the run_id in the graph
    graph_data = json.loads(graph_path.read_text(encoding="utf-8"))
    graph_data["run_id"] = run_id
    graph_path.write_text(json.dumps(graph_data, indent=2), encoding="utf-8")
    
    # Git commit the seeded graph to allow autoloop keep/revert
    try:
        subprocess.run(["git", "add", str(graph_path)], cwd=REPO, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", f"mirage: baseline graph for {run_id}"], cwd=REPO, check=True, capture_output=True)
    except subprocess.CalledProcessError:
        pass # Ignore if no changes or git isn't configured
    
    # Launch bbctl/autoloop
    autoloop_script = REPO / "tools" / "scripts" / "autoloop.py"
    if autoloop_script.exists():
        print(f"  Launching autonomous loop for {program}...")
        subprocess.run([sys.executable, str(autoloop_script), "--program", program, "--run-id", run_id, "--iterations", "1"], cwd=REPO)
    else:
        print("✗ autoloop.py not found.")

def cmd_scan(args):
    initiate_scan(args.program, is_recon_only=False)
    
def cmd_recon(args):
    initiate_scan(args.program, is_recon_only=True)

def cmd_report(args):
    """Generate a report leveraging the Findings DB."""
    reporter_script = REPO / "tools" / "scripts" / "reporter.py"
    if reporter_script.exists():
        print(f"▶ Generating report for {args.program}...")
        subprocess.run([sys.executable, str(reporter_script), args.program], cwd=REPO)
    else:
        print("✗ reporter.py not found.")

def cmd_research(args):
    """Run OSINT web research for a program."""
    prog_dir = REPO / "programs" / args.program
    if not prog_dir.exists():
        print(f"✗ Program '{args.program}' does not exist.")
        sys.exit(1)
    
    research_dir = prog_dir / "research"
    research_dir.mkdir(exist_ok=True)
    
    print(f"▶ Running OSINT research for {args.program}...")
    print(f"  Research artifacts will be saved to: programs/{args.program}/research/")
    print(f"  Agent prompt: agents/web_researcher.md")
    print("")
    print("  To run research, invoke the web_researcher agent with:")
    print(f"    - Program: {args.program}")
    print(f"    - Scope: programs/{args.program}/scope.yaml")
    print(f"    - Targets: programs/{args.program}/targets.txt")
    print(f"    - Tool outputs: programs/{args.program}/tool_outputs/ (if any)")
    print(f"  The agent should output RESEARCH_JSON to: {research_dir}/")

def cmd_validate(args):
    """Run validation phase for a program."""
    prog_dir = REPO / "programs" / args.program
    if not prog_dir.exists():
        print(f"✗ Program '{args.program}' does not exist.")
        sys.exit(1)
        
    print(f"▶ Validating findings for {args.program}...")
    print(f"  Agent prompt: agents/validator.md")
    print("")
    print("  To run validation, invoke the validator agent with:")
    print(f"    - Program: {args.program}")
    print(f"    - Scope: programs/{args.program}/scope.yaml")

def main():
    ensure_dirs()
    
    parser = argparse.ArgumentParser(description="Mirage Bug Bounty AI System")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Program subparser
    parser_program = subparsers.add_parser("program", help="Manage programs")
    prog_subs = parser_program.add_subparsers(dest="subcommand", required=True)
    
    p_create = prog_subs.add_parser("create", help="Create a new program")
    p_create.add_argument("name", help="Name of the program")
    
    p_list = prog_subs.add_parser("list", help="List all programs")
    
    # Scan subparser
    parser_scan = subparsers.add_parser("scan", help="Run a full scan on a program")
    parser_scan.add_argument("program", help="Target program name")
    
    # Recon subparser
    parser_recon = subparsers.add_parser("recon", help="Run a recon-only scan on a program")
    parser_recon.add_argument("program", help="Target program name")
    
    # Report subparser
    parser_report = subparsers.add_parser("report", help="Generate a report for a program")
    parser_report.add_argument("program", help="Target program name")
    
    # Research subparser
    parser_research = subparsers.add_parser("research", help="Run OSINT web research for a program")
    parser_research.add_argument("program", help="Target program name")
    
    # Validate subparser
    parser_validate = subparsers.add_parser("validate", help="Validate findings for a program")
    parser_validate.add_argument("program", help="Target program name")
    
    args = parser.parse_args()
    
    if args.command == "program":
        if args.subcommand == "create":
            cmd_program_create(args)
        elif args.subcommand == "list":
            cmd_program_list(args)
    elif args.command == "scan":
        cmd_scan(args)
    elif args.command == "recon":
        cmd_recon(args)
    elif args.command == "report":
        cmd_report(args)
    elif args.command == "research":
        cmd_research(args)
    elif args.command == "validate":
        cmd_validate(args)

if __name__ == "__main__":
    main()
