from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from app.agents.support import run_support_agent
from app.database import engine, init_db
from app.models import PromptRequest, SupportTicket


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    with Session(engine) as session:
        if not session.exec(select(SupportTicket)).first():
            session.add_all(
                [
                    SupportTicket(
                        category="billing",
                        issue_description="User reporting double charges",
                        status="Open",
                    ),
                    SupportTicket(
                        category="billing",
                        issue_description="Refund request for failed subscription",
                        status="Open",
                    ),
                    SupportTicket(
                        category="technical",
                        issue_description="App crashing on login for iOS users",
                        status="Open",
                    ),
                    SupportTicket(
                        category="shipping",
                        issue_description="Delayed tracking number update",
                        status="Open",
                    ),
                ]
            )
            session.commit()
    yield
    engine.dispose()


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
    agent_output = run_support_agent(request.prompt)
    return {
        "status": "success",
        "user_prompt": request.prompt,
        "agent_response": agent_output,
    }
