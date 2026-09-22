import pytest
from app.db.base import async_session
from app.db.models import SupportTicket, TicketStatus


@pytest.mark.asyncio
async def test_create_support_ticket():
    async with async_session() as session:
        ticket = SupportTicket(
            user_email="test@example.com",
            subject="Test subject",
            description="Test description",
            status=TicketStatus.OPEN,
        )
        session.add(ticket)
        await session.flush()
        assert ticket.id is not None
