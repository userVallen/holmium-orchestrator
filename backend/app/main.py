from contextlib import asynccontextmanager
from uuid import UUID

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.genai.errors import APIError

from app.agents.support import (
    SyncSession,
    fetch_chats,
    fetch_messages,
    run_support_agent,
)
from app.database import engine
from app.db.models import Chat as ChatModel
from app.dtos import Chat, ChatRequest, ChatResponse, Message


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(title="Holmium Orchestrator API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)


@app.get("/api/chats", response_model=list[Chat])
def get_user_chats(user_id: UUID):
    try:
        chats = fetch_chats(user_id)
        return chats
    except APIError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/chats/{session_id}/messages", response_model=list[Message])
def get_chat_messages(session_id: UUID):
    with SyncSession() as session:
        chat_exists = session.get(ChatModel, session_id)
        if not chat_exists:
            raise HTTPException(status_code=404, detail="Chat session not found")

    try:
        messages = fetch_messages(session_id)
        return messages
    except APIError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/agent/run", response_model=ChatResponse)
def run_agent(request: ChatRequest):
    try:
        agent_output = run_support_agent(request.session_id, request.prompt)
        return {"session_id": request.session_id, "agent_response": agent_output}
    except APIError as e:
        raise HTTPException(status_code=500, detail=f"Gemini Error: {e}")
