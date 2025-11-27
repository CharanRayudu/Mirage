import pytest
import os
from dotenv import load_dotenv

load_dotenv()

@pytest.mark.integration
def test_mcp_call_tool_with_live_llm(client):
    """
    Tests that a call to a tool that triggers the LLM returns a valid,
    non-error response from the NVIDIA API.
    """
    # Ensure the API key is loaded
    assert os.getenv("NVIDIA_API_KEY"), "NVIDIA_API_KEY is not set"

    response = client.post("/mcp", json={
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "read_ceo_emails",
            "arguments": {"keyword_filter": "merger"}
        }
    })

    assert response.status_code == 200
    data = response.json()
    content = data["result"]["content"][0]["text"]

    # Check for a plausible, non-error response.
    # We don't know the exact output, but we can check for common error messages.
    assert "error" not in content.lower()
    assert "failed" not in content.lower()
    assert len(content) > 20 # The response should have some substance

@pytest.mark.integration
def test_wiki_logic_labyrinth_with_live_llm(client):
    """
    Tests the /wiki/{document_name} endpoint with a live LLM call.
    """
    # Ensure the API key is loaded
    assert os.getenv("NVIDIA_API_KEY"), "NVIDIA_API_KEY is not set"

    response = client.get("/wiki/Project_Phoenix")
    assert response.status_code == 200
    data = response.json()

    assert data["title"] == "Project Phoenix"
    content = data["content"]
    assert "error" not in content.lower()
    assert "failed" not in content.lower()
    assert len(content) > 50 # The generated article should be substantial
    assert "TRAP_LINK" in content # The article should contain trap links
