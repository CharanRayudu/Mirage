"""
parse_nuclei.py — Parse Nuclei JSONL output into normalized findings.

Reads Nuclei's JSON-lines output and converts each finding into a
standardized format compatible with findings.db.

Usage:
    python tools/adapters/parse_nuclei.py <nuclei_output.jsonl>
"""
import json
import sys
from pathlib import Path


SEVERITY_MAP = {
    "critical": "critical",
    "high": "high",
    "medium": "medium",
    "low": "low",
    "info": "info",
    "unknown": "info",
}


def parse_nuclei_line(line: str) -> dict | None:
    """Parse a single Nuclei JSONL line into a normalized finding."""
    try:
        data = json.loads(line.strip())
    except json.JSONDecodeError:
        return None

    if not data.get("template-id"):
        return None

    return {
        "title": f"[{data.get('template-id', 'unknown')}] {data.get('info', {}).get('name', 'Unnamed')}",
        "severity": SEVERITY_MAP.get(data.get("info", {}).get("severity", "info"), "info"),
        "category": data.get("type", ""),
        "description": data.get("info", {}).get("description", ""),
        "matched_at": data.get("matched-at", ""),
        "matcher_name": data.get("matcher-name", ""),
        "template_id": data.get("template-id", ""),
        "host": data.get("host", ""),
        "ip": data.get("ip", ""),
        "timestamp": data.get("timestamp", ""),
        "curl_command": data.get("curl-command", ""),
        "extracted_results": data.get("extracted-results", []),
        "tags": data.get("info", {}).get("tags", []),
        "reference": data.get("info", {}).get("reference", []),
        "remediation": data.get("info", {}).get("remediation", ""),
    }


def parse_file(filepath: Path) -> list[dict]:
    """Parse a full Nuclei JSONL file."""
    findings = []
    with filepath.open("r", encoding="utf-8") as f:
        for line in f:
            finding = parse_nuclei_line(line)
            if finding:
                findings.append(finding)
    return findings


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python parse_nuclei.py <nuclei_output.jsonl>")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"File not found: {filepath}")
        sys.exit(1)

    findings = parse_file(filepath)
    print(json.dumps(findings, indent=2))
    print(f"\nParsed {len(findings)} finding(s) from {filepath.name}")


if __name__ == "__main__":
    main()
