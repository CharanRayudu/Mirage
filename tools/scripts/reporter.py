#!/usr/bin/env python3
"""
reporter.py — Mirage Report Generator

Queries the program's findings.db for vulnerabilities and generates a Markdown report.
"""
import sqlite3
import argparse
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]

def generate_report(program: str) -> None:
    db_path = REPO / "programs" / program / "findings.db"
    if not db_path.exists():
        print(f"✗ Database not found for program '{program}': {db_path}")
        return

    report_dir = REPO / "reports" / program
    report_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = time.strftime("%Y_%m_%d")
    report_file = report_dir / f"report_{timestamp}.md"
    
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT * FROM vulnerabilities WHERE status != 'false_positive' ORDER BY severity ASC")
        findings = cur.fetchall()
    except sqlite3.OperationalError as e:
        print(f"✗ Database error (perhaps it's empty?): {e}")
        return
        
    lines = []
    lines.append(f"# Mirage Security Assessment Report")
    lines.append(f"**Program:** {program}")
    lines.append(f"**Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append("## Executive Summary")
    lines.append(f"Total findings: {len(findings)}")
    lines.append("")
    
    if len(findings) == 0:
        lines.append("*No valid vulnerabilities were found during this assessment.*")
    else:
        for idx, row in enumerate(findings, 1):
            vuln_id = row["id"]
            title = row["title"]
            severity = str(row["severity"]).upper()
            status = row["status"]
            desc = row["description"]
            impact = row["impact"]
            reproduction = row["reproduction"]
            
            lines.append(f"### {idx}. {title} ({severity})")
            lines.append(f"**Status:** {status}")
            lines.append("")
            
            # Since target might not be hardcoded in the vulnerability row directly (we just have node_id etc), we specify what's there
            lines.append("#### Description")
            lines.append(f"{desc}")
            lines.append("")
            
            lines.append("#### Impact")
            lines.append(f"{impact}")
            lines.append("")
            
            lines.append("#### Reproduction Steps")
            lines.append(f"{reproduction}")
            lines.append("")
            
            # Fetch evidence
            try:
                cur.execute("SELECT * FROM evidence WHERE vulnerability_id = ?", (vuln_id,))
                evidence_items = cur.fetchall()
                if evidence_items:
                    lines.append("#### Evidence")
                    for ev in evidence_items:
                        lines.append(f"- **{ev['evidence_type']}**: `{ev['artifact_path']}`")
                        if ev["description"]:
                            lines.append(f"  - {ev['description']}")
                    lines.append("")
            except sqlite3.OperationalError:
                pass
                
            lines.append("---")
            lines.append("")
            
    conn.close()
    
    report_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"✓ Report generated: {report_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mirage Report Generator")
    parser.add_argument("program", help="Target program name")
    args = parser.parse_args()
    
    generate_report(args.program)
