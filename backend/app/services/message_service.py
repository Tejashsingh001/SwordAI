"""Application service functions for Message CRUD operations."""

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.message import Message
from app.repositories.message_repository import MessageRepository
from app.schemas.message import MessageCreate
from app.services import conversation_service


def create_message(message: MessageCreate, db: Session) -> Message:
    """Create and return a conversation message."""
    repository = MessageRepository(db)
    db_message = repository.create(
        message.conversation_id,
        message.role,
        message.content,
    )

    if db_message.role == "user":
        conversation_service.refresh_conversation_summary(
            db_message.conversation_id,
            db,
        )

    return db_message


def get_messages(db: Session) -> list[Message]:
    """Return every stored message."""
    return MessageRepository(db).get_all()


def get_message(message_id: int, db: Session) -> Message:
    """Return one message or raise the existing-style 404 response."""
    message = MessageRepository(db).get_by_id(message_id)

    if message is None:
        raise HTTPException(
            status_code=404,
            detail="Message not found",
        )

    return message


def get_conversation_messages(
    conversation_id: int,
    db: Session,
) -> list[Message]:
    """Return all messages belonging to one conversation."""
    return MessageRepository(db).get_by_conversation_id(conversation_id)


def update_message(
    message_id: int,
    message: MessageCreate,
    db: Session,
) -> Message:
    """Update and return one message or raise a 404 response."""
    repository = MessageRepository(db)
    db_message = repository.get_by_id(message_id)

    if db_message is None:
        raise HTTPException(
            status_code=404,
            detail="Message not found",
        )

    summary_conversation_ids = {
        db_message.conversation_id
        if db_message.role == "user"
        else None,
        message.conversation_id if message.role == "user" else None,
    }
    updated_message = repository.update(
        db_message,
        message.conversation_id,
        message.role,
        message.content,
    )

    for conversation_id in summary_conversation_ids - {None}:
        conversation_service.refresh_conversation_summary(conversation_id, db)

    return updated_message


def delete_message(message_id: int, db: Session) -> dict[str, str]:
    """Delete one message or raise a 404 response."""
    repository = MessageRepository(db)
    db_message = repository.get_by_id(message_id)

    if db_message is None:
        raise HTTPException(
            status_code=404,
            detail="Message not found",
        )

    conversation_id = db_message.conversation_id
    should_refresh_summary = db_message.role == "user"
    repository.delete(db_message)

    if should_refresh_summary:
        conversation_service.refresh_conversation_summary(conversation_id, db)

    return {"message": "Message deleted successfully"}
