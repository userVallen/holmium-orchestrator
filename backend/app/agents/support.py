from google import genai
from google.genai import types
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.db.models import SupportTicket
from app.models.enums import TicketCategory

sync_engine = create_engine(settings.database_url_sync)
SyncSession = sessionmaker(bind=sync_engine)

client = genai.Client(api_key=settings.gemini_api_key)


class TicketExtractionResult(BaseModel):
    user_email: EmailStr = Field(
        description="The user's email address if present in the text, otherwise a placeholder or fallback email."
    )
    subject: str = Field(
        description="A short, concise summary or title for the support ticket."
    )
    description: str = Field(
        description="The cleaned-up core issue or request details."
    )
    category: TicketCategory = Field(
        description="The classified category of the support ticket."
    )


def create_support_ticket(ticket: TicketExtractionResult) -> str:
    """Creates a new customer support ticket in the PostgreSQL database.

    Args:
        ticket: The structured ticket data containing the user's email, subject, description, and category.
    """
    with SyncSession() as session:
        db_ticket = SupportTicket(
            user_email=ticket.user_email,
            subject=ticket.subject,
            description=ticket.description,
            category=ticket.category.value,
        )
        session.add(db_ticket)
        session.commit()
        session.refresh(db_ticket)

        return f"Successfully created support ticket #{db_ticket.id} under category '{ticket.category.value}'."


def query_support_ticket(category: str) -> str:
    """Queries the PostgreSQL company database for customer support tickets based on category.

    Args:
        category: The ticket category, e.g., 'billing', 'technical', 'account', 'feature_request', 'general'.
    """
    with SyncSession() as session:
        statement = select(SupportTicket).where(
            SupportTicket.category.ilike(f"%{category}%")
        )
        tickets = session.scalars(statement).all()

        if not tickets:
            return f"No tickets found for category: {category}"

        formatted_tickets = [f"- [{t.status}] {t.description}" for t in tickets]
        return f"Found {len(tickets)} open tickets:\n" + "\n".join(formatted_tickets)


def run_support_agent(prompt: str) -> str:
    chat = client.chats.create(
        model=settings.fast_model,
        config=types.GenerateContentConfig(
            temperature=0.2, tools=[create_support_ticket, query_support_ticket]
        ),
    )
    response = chat.send_message(prompt)
    return response.text
