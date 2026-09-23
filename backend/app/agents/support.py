from google import genai
from google.genai import types
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.db.models import SupportTicket

sync_engine = create_engine(settings.database_url_sync)
SyncSession = sessionmaker(bind=sync_engine)

client = genai.Client(api_key=settings.gemini_api_key)


def query_support_ticket(category: str) -> str:
    """Queries the PostgreSQL company database for customer support tickets based on category.

    Args:
        category: The ticket category, e.g., 'billing', 'technical', 'shipping'
    """
    with SyncSession() as session:
        statement = select(SupportTicket).where(
            SupportTicket.category.ilike(f"%{category}%")
        )
        tickets = session.scalar(statement).all()

        if not tickets:
            return f"No tickets found for category: {category}"

        formatted_tickets = [f"- [{t.status}] {t.issue_description}" for t in tickets]
        return f"Found {len(tickets)} open tickets:\n" + "\n".join(formatted_tickets)


def run_support_agent(prompt: str) -> str:
    chat = client.chats.create(
        model=settings.fast_model,
        config=types.GenerateContentConfig(
            temperature=0.2, tools=[query_support_ticket]
        ),
    )
    response = chat.send_message(prompt)
    return response.text
