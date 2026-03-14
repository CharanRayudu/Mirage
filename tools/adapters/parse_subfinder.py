#!/usr/bin/env python3
"""
Parses subfinder output and converts it into a Mirage-compatible JSON format.
Expected input: Standard subfinder output (one subdomain per line)
"""
import sys
import json

def parse_subfinder(input_lines):
    discoveries = []
    for line in input_lines:
        subdomain = line.strip()
        if not subdomain:
            continue
            
        discoveries.append({
            "type": "subdomain",
            "value": subdomain,
            "source": "subfinder"
        })
        
    return discoveries

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Read from file
        try:
            with open(sys.argv[1], "r") as f:
                lines = f.readlines()
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.exit(1)
    else:
        # Read from stdin
        lines = sys.stdin.readlines()
        
    results = parse_subfinder(lines)
    print(json.dumps(results, indent=2))
