from contextlib import asynccontextmanager
from unicodedata import category

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.genai.errors import APIError
from sqlmodel import Session

from app.agents.support import run_support_agent, create_support_ticket
from app.database import engine
from app.dtos import PromptRequest, TicketResponse
from app.db.base import get_db
from app.db.models import SupportTicket


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


@app.post("/api/agent/run")
def run_agent(request: PromptRequest):
    try:
        agent_output = run_support_agent(request.prompt)
        return agent_output
    except APIError as e:
        raise HTTPException(status_code=500, detail=f"Gemini Error: {e}")
