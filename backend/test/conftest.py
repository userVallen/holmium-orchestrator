import os
import uuid

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine

env_test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.env.test"))
load_dotenv(env_test_path, override=True)

import pytest_asyncio
from app.db import base as db_base
from app.db.models import Chat, Message, User
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Switch to test DB
test_db_async = os.getenv("DATABASE_URL_ASYNC")
if not test_db_async:
    raise RuntimeError("DATABASE_URL_ASYNC is not set after loading .env.test")

test_db_sync = os.getenv("DATABASE_URL_SYNC")
if not test_db_sync:
    raise RuntimeError("DATABASE_URL_SYNC is not set after loading .env.test")


async_engine_kwargs: dict = {"echo": False}
if test_db_async.startswith("sqlite"):
    async_engine_kwargs["connect_args"] = {
        "check_same_thread": False
    }  # Allow FastAPI/Pytest to switch threads during async operations
    async_engine_kwargs["poolclass"] = (
        StaticPool  # Force SQLAlchemy to use a permanent connection across the test lifecycle
    )

sync_engine_kwargs: dict = {"echo": False}
if test_db_sync.startswith("sqlite"):
    sync_engine_kwargs["connect_args"] = {
        "check_same_thread": False
    }  # Allow FastAPI/Pytest to switch threads during async operations
    sync_engine_kwargs["poolclass"] = (
        StaticPool  # Force SQLAlchemy to use a permanent connection across the test lifecycle
    )

# Switch engine and session to use the test DB
test_async_engine = create_async_engine(test_db_async, **async_engine_kwargs)
db_base.async_engine = test_async_engine
db_base.async_session = sessionmaker(
    test_async_engine, class_=AsyncSession, expire_on_commit=False
)

test_sync_engine = create_engine(test_db_sync, **sync_engine_kwargs)
db_base.sync_engine = test_sync_engine
db_base.sync_session = sessionmaker(bind=test_sync_engine)


@pytest_asyncio.fixture(autouse=True)
async def setup_test_db():
    async with db_base.async_engine.begin() as conn:
        await conn.run_sync(db_base.Base.metadata.create_all)
    yield
    async with db_base.async_engine.begin() as conn:
        await conn.run_sync(db_base.Base.metadata.drop_all)


# Clean up test.db at the start and end of testing
@pytest.fixture(scope="session", autouse=True)
def clean_test_db_file():
    db_file = "test.db"
    if os.path.exists(db_file):
        os.remove(db_file)
    yield
    if os.path.exists(db_file):
        os.remove(db_file)


@pytest.fixture
def seeded_chat():
    with db_base.sync_session() as session:
        dummy_user_id = uuid.uuid4()
        user = User(id=dummy_user_id, name="Test user", email="test@example.com")
        session.add(user)

        chat = Chat(
            user_id=user.id,
            title="Test chat",
        )
        session.add(chat)
        session.commit()

        user_prompt = Message(session_id=chat.id, role="user", content="Test prompt")
        agent_response = Message(
            session_id=chat.id, role="agent", content="Test response"
        )
        session.add_all([user_prompt, agent_response])
        session.commit()

        return {"session_id": chat.id, "user_id": chat.user_id}
