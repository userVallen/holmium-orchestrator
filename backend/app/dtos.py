from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.enums import TicketCategory, TicketStatus


class TicketResponse(BaseModel):
    id: str
    user_email: str
    subject: str
    description: str
    status: TicketStatus
    category: TicketCategory

    model_config = ConfigDict(from_attributes=True)


class ChatRequest(BaseModel):
    session_id: str
    prompt: str


class ChatResponse(BaseModel):
    session_id: str
    agent_response: str


class Chat(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Message(BaseModel):
    id: UUID
    session_id: UUID
    role: str
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
