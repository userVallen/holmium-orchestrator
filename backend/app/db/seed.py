import asyncio

from sqlalchemy import select

from app.db.base import async_session
from app.db.models import SupportTicket, TicketStatus


async def seed_db():
    async with async_session() as session:
        result = await session.execute(
            select(SupportTicket).where(SupportTicket.user_email == "user1@example.com")
        )
        existing_ticket = result.scalars().first()

        if existing_ticket:
            print("Database is already seeded. Skipping insertion. ⏩")
            return

        ticket1 = SupportTicket(
            user_email="user1@example.com",
            subject="Login issue",
            description="I cannot log into my account using Google SSO.",
            status=TicketStatus.OPEN,
        )
        ticket2 = SupportTicket(
            user_email="user2@example.com",
            subject="Billing question",
            description="Where can I download my latest invoice?",
            status=TicketStatus.IN_PROGRESS,
        )
        session.add_all([ticket1, ticket2])
        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed_db())
