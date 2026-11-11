import uuid
from unittest.mock import patch

from app.main import app
from fastapi.testclient import TestClient
from google.genai.errors import APIError

client = TestClient(app)


@patch("app.main.run_support_agent")
def test_run_agent_success(mock_run):
    mock_run.return_value = "test response"

    response = client.post(
        "/api/agent/run",
        json={"session_id": "test session id", "prompt": "test prompt"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "session_id": "test session id",
        "agent_response": "test response",
    }


def test_run_agent_missing_prompt():
    response = client.post("/api/agent/run", json={})

    assert response.status_code == 422


def test_get_user_chats_success(seeded_chat):
    response = client.get("/api/chats", params={"user_id": seeded_chat["user_id"]})

    assert response.status_code == 200


def test_get_user_chats_missing_parameter():
    response = client.get("/api/chats")

    assert response.status_code == 422


def test_get_chat_messages_success(seeded_chat):
    session_id = seeded_chat["session_id"]
    response = client.get(f"/api/chats/{session_id}/messages")

    assert response.status_code == 200
    assert len(response.json()) > 0
    assert isinstance(response.json(), list)


def test_get_chat_messages_invalid_session_id():
    session_id = uuid.NIL
    response = client.get(f"/api/chats/{session_id}/messages")

    assert response.status_code == 404


@patch("app.main.run_support_agent")
def test_run_agent_gemini_failure(mock_run):
    mock_run.side_effect = APIError(
        code=429,
        response_json={"error": {"message": "API rate limit exceeded"}},
    )

    response = client.post(
        "/api/agent/run",
        json={"session_id": "test session id", "prompt": "test prompt"},
    )

    assert response.status_code == 500
