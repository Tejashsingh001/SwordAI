"""HTTP endpoints for conversation message CRUD operations."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.schemas.message import MessageCreate, MessageResponse
from app.services import message_service

router = APIRouter(
    prefix="/messages",
    tags=["Messages"],
)


@router.post("/", response_model=MessageResponse)
def create_message(
    message: MessageCreate,
    db: Session = Depends(get_db),
) -> MessageResponse:
    """Create a message associated with a conversation."""
    return message_service.create_message(message, db)


@router.get("/", response_model=list[MessageResponse])
def get_messages(
    db: Session = Depends(get_db),
) -> list[MessageResponse]:
    """Return all messages."""
    return message_service.get_messages(db)


@router.get(
    "/conversation/{conversation_id}",
    response_model=list[MessageResponse],
)
def get_conversation_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
) -> list[MessageResponse]:
    """Return all messages belonging to one conversation."""
    return message_service.get_conversation_messages(conversation_id, db)


@router.get("/{message_id}", response_model=MessageResponse)
def get_message(
    message_id: int,
    db: Session = Depends(get_db),
) -> MessageResponse:
    """Return one message by ID."""
    return message_service.get_message(message_id, db)


@router.put("/{message_id}", response_model=MessageResponse)
def update_message(
    message_id: int,
    message: MessageCreate,
    db: Session = Depends(get_db),
) -> MessageResponse:
    """Update one message by ID."""
    return message_service.update_message(message_id, message, db)


@router.delete("/{message_id}")
def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
) -> dict[str, str]:
    """Delete one message by ID."""
    return message_service.delete_message(message_id, db)
