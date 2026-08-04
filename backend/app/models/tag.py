"""SQLAlchemy models for reusable conversation tags."""

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.database.database import Base

conversation_tags = Table(
    "conversation_tags",
    Base.metadata,
    Column("conversation_id", ForeignKey("conversations.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class Tag(Base):
    """Represent a reusable label that can be attached to conversations."""

    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)

    conversations = relationship(
        "Conversation",
        secondary=conversation_tags,
        back_populates="tags",
    )
