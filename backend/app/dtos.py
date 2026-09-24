from pydantic import BaseModel

from app.models.enums import TicketCategory, TicketStatus


class TicketResponse(BaseModel):
    id: str
    user_email: str
    subject: str
    description: str
    status: TicketStatus
    category: TicketCategory

    class Config:
        from_attributes = True


class PromptRequest(BaseModel):
    prompt: str
