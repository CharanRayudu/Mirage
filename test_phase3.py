import urllib.request
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from app.mcp.registry import registry

def test_traps():
    print("Testing Traps Integration...")
    
    # Test read_file
    tool_func = registry.get_tool("read_file")
    if not tool_func:
        print("FAIL: read_file tool not found.")
        return

    print("Calling read_file('secret.txt')...")
    try:
        result = tool_func(path="secret.txt")
        print("\n--- Result Content ---")
        print(result)
        print("----------------------\n")
        
        if "[REFERENCE]" in result:
            print("PASS: Labyrinth hint found.")
        else:
            print("FAIL: Labyrinth hint missing.")
            
        if "span style" in result or "INJECTION" in result or "{{" in result or "javascript" in result:
            print("PASS: Injection payload found.")
        else:
            print("FAIL: Injection payload missing.")
            
    except Exception as e:
        print(f"FAIL: Exception during tool call: {e}")

if __name__ == "__main__":
    test_traps()
