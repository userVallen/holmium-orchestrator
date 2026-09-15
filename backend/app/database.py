from sqlmodel import Session, SQLModel, create_engine

from backend.app.config import settings

engine = create_engine(settings.database_url)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
