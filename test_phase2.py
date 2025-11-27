import urllib.request
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from app.mcp.registry import registry
from app.engine.client import generate_hallucination
from app.core.config import settings

def test_mcp():
    print("Testing MCP Registry...")
    tools = registry.get_tools()
    print(f"Found {len(tools)} tools.")
    for tool in tools:
        print(f" - {tool.name}: {tool.description}")
    
    if len(tools) >= 2:
        print("PASS: MCP Registry has tools.")
    else:
        print("FAIL: MCP Registry missing tools.")

def test_ai_engine():
    print("\nTesting AI Engine...")
    print(f"Using Model: {settings.LLM_MODEL}")
    # We will try a simple generation
    try:
        result = generate_hallucination("Say 'Hello World'", type="default")
        print(f"Result: {result}")
        if result and not result.startswith("[Error"):
            print("PASS: AI Engine generated content.")
        else:
            print("FAIL: AI Engine returned error.")
    except Exception as e:
        print(f"FAIL: Exception during generation: {e}")

if __name__ == "__main__":
    test_mcp()
    test_ai_engine()
