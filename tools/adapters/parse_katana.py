#!/usr/bin/env python3
"""
Parses katana output (JSON format) and converts it into a Mirage-compatible JSON format.
Expected input: katana output using `-j` flag.
"""
import sys
import json

def parse_katana(input_lines):
    discoveries = []
    for line in input_lines:
        line = line.strip()
        if not line:
            continue
            
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue
            
        url = data.get("request", {}).get("endpoint", "") or data.get("endpoint", "")
        if not url:
            continue
            
        discoveries.append({
            "type": "endpoint",
            "value": url,
            "method": data.get("request", {}).get("method", "GET"),
            "source": "katana"
        })
        
    return discoveries

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            with open(sys.argv[1], "r") as f:
                lines = f.readlines()
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.exit(1)
    else:
        lines = sys.stdin.readlines()
        
    results = parse_katana(lines)
    print(json.dumps(results, indent=2))
