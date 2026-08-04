"""SQLAlchemy repository for Message persistence operations."""

from sqlalchemy.orm import Session

from app.models.message import Message


class MessageRepository:
    """Provide database access methods for Message records only."""

    def __init__(self, db: Session) -> None:
        """Initialize the repository with an injected SQLAlchemy session."""
        self.db = db

    def create(
        self,
        conversation_id: int,
        role: str,
        content: str,
    ) -> Message:
        """Create, commit, and return a message record."""
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)

        return message

    def get_all(self) -> list[Message]:
        """Return every message record."""
        return self.db.query(Message).all()

    def get_by_id(self, message_id: int) -> Message | None:
        """Return a message by ID when it exists."""
        return self.db.query(Message).filter(Message.id == message_id).first()

    def get_by_conversation_id(self, conversation_id: int) -> list[Message]:
        """Return every message belonging to one conversation."""
        return self.db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc()).all()

    def get_user_messages_by_conversation_id(
        self,
        conversation_id: int,
    ) -> list[Message]:
        """Return user messages in chronological order for one conversation."""
        return self.db.query(Message).filter(
            Message.conversation_id == conversation_id,
            Message.role == "user",
        ).order_by(Message.created_at.asc()).all()

    def count_by_conversation_id(self, conversation_id: int) -> int:
        """Count every message belonging to one conversation."""
        return self.db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).count()

    def count_by_conversation_and_role(
        self,
        conversation_id: int,
        role: str,
    ) -> int:
        """Count messages for one conversation and author role."""
        return self.db.query(Message).filter(
            Message.conversation_id == conversation_id,
            Message.role == role,
        ).count()

    def update(
        self,
        message: Message,
        conversation_id: int,
        role: str,
        content: str,
    ) -> Message:
        """Update, commit, and return an existing message."""
        message.conversation_id = conversation_id
        message.role = role
        message.content = content
        self.db.commit()
        self.db.refresh(message)

        return message

    def delete(self, message: Message) -> None:
        """Delete and commit an existing message."""
        self.db.delete(message)
        self.db.commit()
