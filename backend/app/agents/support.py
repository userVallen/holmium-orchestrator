from google import genai
from google.genai import types
from sqlmodel import Session, select

from backend.app.config import settings
from backend.app.database import engine
from backend.app.models import SupportTicket

client = genai.Client(api_key=settings.gemini_api_key)


def query_support_ticket(category: str) -> str:
    """Queries the PostgreSQL company database for customer support tickets based on category.

    Args:
        category: The ticket category, e.g., 'billing', 'technical', 'shipping'
    """
    with Session(engine) as session:
        statement = select(SupportTicket).where(
            SupportTicket.category.ilike(f"%{category}%")
        )
        tickets = session.exec(statement).all()

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
