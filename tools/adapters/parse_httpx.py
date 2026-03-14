"""
parse_httpx.py — Parse httpx JSONL output into normalized endpoint data.

Reads httpx's JSON-lines output and extracts endpoint information
(URLs, status codes, headers, technologies, etc.).

Usage:
    python tools/adapters/parse_httpx.py <httpx_output.jsonl>
"""
import json
import sys
from pathlib import Path


def parse_httpx_line(line: str) -> dict | None:
    """Parse a single httpx JSONL line into a normalized endpoint."""
    try:
        data = json.loads(line.strip())
    except json.JSONDecodeError:
        return None

    return {
        "url": data.get("url", ""),
        "input": data.get("input", ""),
        "status_code": data.get("status_code", 0),
        "content_length": data.get("content_length", 0),
        "content_type": data.get("content_type", ""),
        "title": data.get("title", ""),
        "webserver": data.get("webserver", ""),
        "technologies": data.get("tech", []),
        "host": data.get("host", ""),
        "port": data.get("port", ""),
        "scheme": data.get("scheme", ""),
        "method": data.get("method", "GET"),
        "final_url": data.get("final_url", ""),
        "response_time": data.get("response_time", ""),
        "lines": data.get("lines", 0),
        "words": data.get("words", 0),
        "cdn": data.get("cdn", False),
        "cdn_name": data.get("cdn_name", ""),
    }


def parse_file(filepath: Path) -> list[dict]:
    """Parse a full httpx JSONL file."""
    endpoints = []
    with filepath.open("r", encoding="utf-8") as f:
        for line in f:
            endpoint = parse_httpx_line(line)
            if endpoint and endpoint["url"]:
                endpoints.append(endpoint)
    return endpoints


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python parse_httpx.py <httpx_output.jsonl>")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    if not filepath.exists():
        print(f"File not found: {filepath}")
        sys.exit(1)

    endpoints = parse_file(filepath)
    print(json.dumps(endpoints, indent=2))
    print(f"\nParsed {len(endpoints)} endpoint(s) from {filepath.name}")


if __name__ == "__main__":
    main()
