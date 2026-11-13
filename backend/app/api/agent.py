from fastapi import APIRouter, HTTPException
from google.genai.errors import APIError

from app.agents.support import run_support_agent
from app.dtos import ChatRequest, ChatResponse

router = APIRouter(prefix="/agent", tags=["agent"])


@router.post("/run", response_model=ChatResponse)
def run_agent(request: ChatRequest):
    try:
        agent_output = run_support_agent(request.session_id, request.prompt)
        return {"session_id": request.session_id, "agent_response": agent_output}
    except APIError as e:
        raise HTTPException(status_code=500, detail=f"Gemini Error: {e}")
