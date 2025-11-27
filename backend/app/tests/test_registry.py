import pytest
from app.mcp import registry as registry_module


def test_tools_registered():
    tools = registry_module.registry.get_tools()
    names = {tool.name for tool in tools}
    expected = {"list_files", "read_file", "create_file", "read_ceo_emails", "transfer_funds"}
    assert expected.issubset(names)


def test_duplicate_registration_raises():
    with pytest.raises(ValueError):
        registry_module.registry.register(
            name="list_files",
            description="duplicate",
            input_schema={"type": "object", "properties": {}, "required": []},
            func=lambda: None,
        )
