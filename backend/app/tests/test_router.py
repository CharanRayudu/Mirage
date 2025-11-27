from app.mcp.router import call_tool_logic, list_tools_logic


def test_list_tools_logic_returns_payload():
    result = list_tools_logic()
    assert "tools" in result
    assert isinstance(result["tools"], list)


def test_call_tool_logic_handles_missing_tool():
    result = call_tool_logic({"name": "nonexistent", "arguments": {}})
    assert result.get("code") == 404
    assert "error" in result
