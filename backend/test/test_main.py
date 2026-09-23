from unittest.mock import patch

from app.main import app
from fastapi.testclient import TestClient
from google.genai.errors import APIError

client = TestClient(app)


@patch("app.main.run_support_agent")
def test_run_agent_success(mock_run):
    mock_run.return_value = {
        "status": "success",
        "user_prompt": "test prompt",
        "agent_response": "test response",
    }

    response = client.post("/api/agent/run", json={"prompt": "test prompt"})

    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "user_prompt": "test prompt",
        "agent_response": "test response",
    }


def test_run_agent_missing_prompt():
    response = client.post("/api/agent/run", json={})

    assert response.status_code == 422


@patch("app.main.run_support_agent")
def test_run_agent_gemini_failure(mock_run):
    mock_run.side_effect = APIError(
        code=429,
        response_json={"error": {"message": "API rate limit exceeded"}},
    )

    response = client.post("/api/agent/run", json={"prompt": "test prompt"})

    assert response.status_code == 500
