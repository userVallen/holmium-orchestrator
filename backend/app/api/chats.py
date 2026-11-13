import uuid

from fastapi import APIRouter, Depends, HTTPException
from google.genai.errors import APIError

from app.agents.support import (
    SyncSession,
    create_chat_session,
    fetch_chats,
    fetch_messages,
)
from app.api.deps import get_current_user_optional
from app.db.models import Chat as ChatModel
from app.dtos import Chat as ChatDto
from app.dtos import Message

router = APIRouter(prefix="/chats", tags=["chats"])


@router.get("/")
def get_user_chats(user_id: uuid.UUID):
    try:
        chats = fetch_chats(user_id)
        return chats
    except APIError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{session_id}/messages", response_model=list[Message])
def get_chat_messages(session_id: uuid.UUID):
    with SyncSession() as session:
        chat_exists = session.get(ChatModel, session_id)
        if not chat_exists:
            raise HTTPException(status_code=404, detail="Chat session not found")

    try:
        messages = fetch_messages(session_id)
        return messages
    except APIError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=ChatDto)
def create_chat(
    title: str,
    user_id: uuid.UUID | None = Depends(get_current_user_optional),  # noqa: B008
):
    try:
        new_chat = create_chat_session(title=title, user_id=user_id)
        return new_chat
    except APIError as e:
        raise HTTPException(status_code=500, detail=str(e))
