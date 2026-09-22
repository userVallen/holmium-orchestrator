import asyncio

from app.db.base import async_session
from app.db.models import SupportTicket, TicketStatus


async def seed_db():
    async with async_session() as session:
        async with session.begin():
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
