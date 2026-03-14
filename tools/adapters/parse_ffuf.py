"""
parse_ffuf.py — Parse ffuf JSON output into normalized findings.

Reads ffuf's JSON output file and extracts discovered endpoints/content.

Usage:
    python tools/adapters/parse_ffuf.py <ffuf_output.json>
"""
import json
import sys
from pathlib import Path


def parse_ffuf_results(data: dict) -> list[dict]:
    """Parse ffuf JSON output into normalized results."""
    results = []
    config = data.get("config", {})
    base_url = config.get("url", "")

    for result in data.get("results", []):
        results.append({
            "url": result.get("url", ""),
            "input": result.get("input", {}),
            "status_code": result.get("status", 0),
            "content_length": result.get("length", 0),
            "content_words": result.get("words", 0),
            "content_lines": result.get("lines", 0),
            "content_type": result.get("content-type", ""),
            "redirect_location": result.get("redirectlocation", ""),
            "result_file": result.get("resultfile", ""),
            "duration_ns": result.get("duration", 0),
            "host": result.get("host", ""),
        })

    return results


def parse_file(filepath: Path) -> list[dict]:
    """Parse a full ffuf JSON output file."""
    data = json.loads(filepath.read_text(encoding="utf-8"))
    return parse_ffuf_results(data)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python parse_ffuf.py <ffuf_output.json>")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"File not found: {filepath}")
        sys.exit(1)

    results = parse_file(filepath)
    print(json.dumps(results, indent=2))
    print(f"\nParsed {len(results)} result(s) from {filepath.name}")


if __name__ == "__main__":
    main()
