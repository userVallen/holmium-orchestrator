from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

async_engine = create_async_engine(settings.database_url_async, echo=True, future=True)
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

sync_engine = create_engine(settings.database_url_sync, echo=True, future=True)
sync_session = sessionmaker(sync_engine, expire_on_commit=False)

Base = declarative_base()


async def get_db():
    async with async_session() as session:
        yield session
