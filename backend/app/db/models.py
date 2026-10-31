import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import TicketCategory, TicketStatus


class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_email = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(
        Enum(TicketStatus, create_type=False), default=TicketStatus.OPEN, nullable=False
    )
    category = Column(
        String,
        default=TicketCategory.GENERAL.value,
        nullable=False,
    )
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class Chat(Base):
    __tablename__ = "chat_sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    user_email: Mapped[str] = mapped_column(String, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    messages: Mapped[list["Message"]] = relationship(
        "Message", back_populates="chat", cascade="all, delete-orphan"
    )


class Message(Base):
    __tablename__ = "chat_messages"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        nullable=False,
    )
    role: Mapped[str] = mapped_column(String, nullable=False)  # e.g., "user" or "model"
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    chat: Mapped[Chat] = relationship("Chat", back_populates="messages")
