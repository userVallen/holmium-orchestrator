import uuid

from app.api.deps import get_current_user_optional
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_create_chat_as_guest():
    response = client.post("/api/chats", params={"title": "Test title"})

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "created_at" in data
    assert data["user_id"] is None
    assert data["title"] == "Test title"
    assert uuid.UUID(data["id"])


def test_create_chat_as_authenticated_user():
    test_user_id = uuid.uuid4()

    # Override the auth dependency to simulate a logged-in user
    app.dependency_overrides[get_current_user_optional] = lambda: test_user_id

    try:
        response = client.post("/api/chats", params={"title": "Test title"})

        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "created_at" in data
        assert data["user_id"] == str(test_user_id)
        assert data["title"] == "Test title"
        assert uuid.UUID(data["id"])
    finally:
        app.dependency_overrides.clear()


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
