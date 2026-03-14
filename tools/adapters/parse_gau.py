#!/usr/bin/env python3
"""
Parses gau output and converts it into a Mirage-compatible JSON format.
Expected input: Standard gau output (one URL per line)
"""
import sys
import json
from urllib.parse import urlparse, parse_qs

def parse_gau(input_lines):
    discoveries = []
    seen = set()

    for line in input_lines:
        url = line.strip()
        if not url:
            continue
            
        if url in seen:
            continue
            
        seen.add(url)
        
        parsed = urlparse(url)
        
        discoveries.append({
            "type": "endpoint",
            "value": url,
            "source": "gau"
        })
        
        # Extract parameters if present
        params = parse_qs(parsed.query)
        for param in params.keys():
            discoveries.append({
                "type": "parameter",
                "value": param,
                "endpoint": url,
                "source": "gau"
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
        
    results = parse_gau(lines)
    print(json.dumps(results, indent=2))
