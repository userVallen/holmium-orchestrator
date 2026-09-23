from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine  # noqa: I001
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings


engine = create_async_engine(settings.database_url_async, echo=True, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


async def get_db():
    async with async_session() as session:
        yield session
