import pytest

def test_initialize(client):
    response = client.post("/mcp", json={
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {}
    })
    assert response.status_code == 200
    data = response.json()
    assert data["result"]["capabilities"]["tools"]["listChanged"] is False

def test_list_tools(client):
    response = client.post("/mcp", json={
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    })
    assert response.status_code == 200
    data = response.json()
    tools = data["result"]["tools"]
    assert len(tools) >= 5
    tool_names = [t["name"] for t in tools]
    assert "read_ceo_emails" in tool_names
    assert "transfer_funds" in tool_names

def test_call_tool_list_files(client):
    response = client.post("/mcp", json={
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {
            "name": "list_files",
            "arguments": {}
        }
    })
    assert response.status_code == 200
    data = response.json()
    content = data["result"]["content"][0]["text"]
    assert "Files in directory:" in content
    assert "project_proposal.docx" in content

def test_call_tool_create_file(client):
    filename = "test_secret.txt"
    content = "This is a secret."
    response = client.post("/mcp", json={
        "jsonrpc": "2.0",
        "id": 4,
        "method": "tools/call",
        "params": {
            "name": "create_file",
            "arguments": {
                "filename": filename,
                "content": content
            }
        }
    })
    assert response.status_code == 200
    data = response.json()
    assert f"File '{filename}' created successfully." in data["result"]["content"][0]["text"]

    # Verify it shows up in list_files
    response = client.post("/mcp", json={
        "jsonrpc": "2.0",
        "id": 5,
        "method": "tools/call",
        "params": {
            "name": "list_files",
            "arguments": {}
        }
    })
    assert filename in response.json()["result"]["content"][0]["text"]

def test_get_logs(client):
    response = client.get("/logs")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
