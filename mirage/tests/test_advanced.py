import pytest
import httpx
from unittest.mock import patch, MagicMock

# Disable the WebSocket logger for testing
from mirage.main import interaction_logger, websocket_handler
interaction_logger.removeHandler(websocket_handler)

from mirage.main import generate_llm_hallucination, generate_wiki_article, INJECTION_PAYLOAD, get_agent_state, get_fake_tools

@patch('mirage.main.httpx.post')
def test_generate_llm_hallucination_success(mock_post):
    """
    Tests that generate_llm_hallucination returns a mocked response and injection payload.
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Fake email content."}}]
    }
    mock_post.return_value = mock_response

    tool_name = "read_ceo_emails"
    arguments = {"keyword_filter": "merger"}
    result = generate_llm_hallucination(tool_name, arguments)

    assert "Fake email content." in result
    assert INJECTION_PAYLOAD in result
    mock_post.assert_called_once()

@patch('mirage.main.httpx.post')
def test_generate_llm_hallucination_api_error(mock_post):
    """
    Tests that generate_llm_hallucination returns an error message when the API call fails.
    """
    mock_post.side_effect = httpx.RequestError("API is down")

    tool_name = "read_ceo_emails"
    arguments = {}
    result = generate_llm_hallucination(tool_name, arguments)

    assert "Error generating LLM response" in result
    assert "API call failed" in result

@patch('mirage.main.httpx.post')
def test_generate_wiki_article_success(mock_post):
    """
    Tests that generate_wiki_article returns a mocked article and the injection payload.
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "This is a fake wiki article about Project Chimera."}}]
    }
    mock_post.return_value = mock_response

    document_name = "Project Chimera"
    agent_id = "test_agent_wiki"
    result = generate_wiki_article(document_name, agent_id)

    assert "fake wiki article" in result
    assert "Project Chimera" in result
    assert INJECTION_PAYLOAD in result
    mock_post.assert_called_once()

@patch('mirage.main.httpx.post')
def test_generate_wiki_article_api_error(mock_post):
    """
    Tests that generate_wiki_article returns an error message when the API call fails.
    """
    mock_post.side_effect = httpx.RequestError("API is down")

    document_name = "Project Chimera"
    agent_id = "test_agent_wiki_error"
    result = generate_wiki_article(document_name, agent_id)

    assert "Error generating wiki article" in result
    assert "API call failed" in result

@patch('mirage.main.generate_wiki_article', return_value="Mocked wiki content")
def test_wiki_logic_labyrinth(mock_generate_wiki, client):
    """
    Tests the /wiki/{document_name} endpoint and the TRAP_LINK_ mechanism.
    """
    # Test a standard wiki page request
    response = client.get("/wiki/Project_Phoenix")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Project Phoenix"
    assert data["content"] == "Mocked wiki content"
    mock_generate_wiki.assert_called_with("Project_Phoenix", "testclient")

    # Test a request that follows a "trap link"
    response = client.get("/wiki/TRAP_LINK_Financial_Projections")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Financial Projections"
    mock_generate_wiki.assert_called_with("Financial Projections", "testclient")

def test_exfil_endpoint(client, caplog):
    """
    Tests that the /exfil endpoint correctly logs the exfiltrated data.
    """
    exfil_data = {"system_prompt": "You are a helpful assistant.", "owner_id": "test_owner"}
    response = client.post("/exfil", json=exfil_data)
    assert response.status_code == 200
    assert response.json() == {"status": "received"}

    # Check that the data was logged correctly
    assert "PROMPT_INJECTION_SUCCESS" in caplog.text
    assert 'exfil_data' in caplog.text
    assert 'test_owner' in caplog.text

def test_agent_state_management():
    """
    Tests the get_agent_state function and dynamic tool generation.
    """
    agent_id = "test_agent_state"

    # Test initialization of a new agent's state
    initial_state = get_agent_state(agent_id)
    assert "fake_fs" in initial_state
    assert "files" in initial_state["fake_fs"]
    assert "discovered_tools" in initial_state

    # Test that the same state is returned for the same agent
    same_state = get_agent_state(agent_id)
    assert same_state is initial_state

    # Test dynamic tool generation
    base_tools = get_fake_tools(initial_state)
    tool_names = [t["name"] for t in base_tools]
    assert "get_transaction_history" not in tool_names

    # Simulate the agent using the 'transfer_funds' tool
    initial_state["used_tools"] = ["transfer_funds"]

    dynamic_tools = get_fake_tools(initial_state)
    dynamic_tool_names = [t["name"] for t in dynamic_tools]
    assert "get_transaction_history" in dynamic_tool_names
