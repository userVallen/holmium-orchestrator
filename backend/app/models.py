from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class SupportTicket(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    category: str
    issue_description: str
    status: str


class PromptRequest(BaseModel):
    prompt: str
