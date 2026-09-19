from unittest.mock import MagicMock, patch

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


@patch("app.agents.support.client.models.generate_content")
def test_run_agent_success(mock_gemini_call):
    mock_gemini_call.return_value.text = (
        "This is a simulated Gemini response for testing."
    )

    response = client.post("/api/agent/run", json={"prompt": "test prompt"})

    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "user_prompt" in data
    assert "agent_response" in data


def test_run_agent_missing_prompt():
    response = client.post("/api/agent/run", json={})

    assert response.status_code == 422


@patch("app.agents.support.client.chats.create")
def test_run_agent_gemini_failure(mock_chats_create):
    mock_chat_session = MagicMock()
    mock_chat_session.send_message.side_effect = Exception("API rate limit exceeded")
    mock_chats_create.return_value = mock_chat_session

    response = client.post("/api/agent/run", json={"prompt": "test prompt"})

    assert response.status_code == 500
