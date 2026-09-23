import os

from dotenv import load_dotenv

env_test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.env.test"))
load_dotenv(env_test_path, override=True)

import pytest_asyncio
from app.db import base as db_base
from app.db.models import SupportTicket  # noqa: F401
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

test_db_async = os.getenv("DATABASE_URL_ASYNC")
if not test_db_async:
    raise RuntimeError("DATABASE_URL_ASYNC is not set after loading .env.test")

engine_kwargs: dict = {"echo": False}
if test_db_async.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}
    engine_kwargs["poolclass"] = StaticPool

test_engine = create_async_engine(test_db_async, **engine_kwargs)
db_base.engine = test_engine
db_base.async_session = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest_asyncio.fixture(autouse=True)
async def setup_test_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(db_base.Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(db_base.Base.metadata.drop_all)
