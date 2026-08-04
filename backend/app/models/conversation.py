"""SQLAlchemy model for project-scoped conversations."""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class Conversation(Base):
    """Persist metadata for a conversation associated with one project."""

    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    summary = Column(String, default="")
    summary_is_manual = Column(Boolean, default=False)
    is_pinned = Column(Boolean, default=False)
    is_archived = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    project_id = Column(Integer, ForeignKey("projects.id"))

    project = relationship("Project", back_populates="conversations")
    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete",
    )
    tags = relationship(
        "Tag",
        secondary="conversation_tags",
        back_populates="conversations",
    )
