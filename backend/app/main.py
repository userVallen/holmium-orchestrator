from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from google.genai.errors import APIError

from app.agents.support import run_support_agent
from app.database import engine
from app.dtos import ChatRequest, ChatResponse


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


@app.post("/api/agent/run", response_model=ChatResponse)
def run_agent(request: ChatRequest):
    try:
        agent_output = run_support_agent(request.session_id, request.prompt)
        return {"session_id": request.session_id, "agent_response": agent_output}
    except APIError as e:
        raise HTTPException(status_code=500, detail=f"Gemini Error: {e}")
