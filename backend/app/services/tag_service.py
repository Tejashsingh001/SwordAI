"""Application service functions for reusable conversation tags."""

import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.models.tag import Tag
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.tag_repository import TagRepository
from app.schemas.tag import TagCreate

logger = logging.getLogger(__name__)


def create_tag(tag: TagCreate, db: Session) -> Tag:
    """Create a reusable tag, rejecting duplicate names."""
    repository = TagRepository(db)
    if repository.get_by_name(tag.name) is not None:
        raise HTTPException(status_code=409, detail="Tag already exists")
    return repository.create(tag.name)


def get_tags(db: Session) -> list[Tag]:
    """Return all reusable tags in alphabetical order."""
    return TagRepository(db).get_all()


def get_tag(tag_id: int, db: Session) -> Tag:
    """Return one tag or raise a 404 response."""
    tag = TagRepository(db).get_by_id(tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


def update_tag(tag_id: int, tag: TagCreate, db: Session) -> Tag:
    """Rename one tag, retaining case-insensitive uniqueness."""
    repository = TagRepository(db)
    db_tag = get_tag(tag_id, db)
    existing = repository.get_by_name(tag.name)
    if existing is not None and existing.id != db_tag.id:
        raise HTTPException(status_code=409, detail="Tag already exists")
    return repository.update(db_tag, tag.name)


def delete_tag(tag_id: int, db: Session) -> dict[str, str]:
    """Delete one tag and its conversation associations."""
    tag = get_tag(tag_id, db)
    TagRepository(db).delete(tag)
    return {"message": "Tag deleted successfully"}


def get_conversation_tags(conversation_id: int, db: Session) -> list[Tag]:
    """Return the reusable tags assigned to one conversation."""
    conversation = _get_conversation(conversation_id, db)
    return list(conversation.tags)


def add_tag_to_conversation(
    conversation_id: int,
    tag_id: int,
    db: Session,
) -> Tag:
    """Assign a reusable tag to a conversation."""
    conversation = _get_conversation(conversation_id, db)
    tag = get_tag(tag_id, db)
    ConversationRepository(db).add_tag(conversation, tag)
    logger.info("Assigned tag_id=%s to conversation_id=%s.", tag_id, conversation_id)
    return tag


def remove_tag_from_conversation(
    conversation_id: int,
    tag_id: int,
    db: Session,
) -> dict[str, str]:
    """Remove a tag association from a conversation."""
    conversation = _get_conversation(conversation_id, db)
    tag = get_tag(tag_id, db)
    ConversationRepository(db).remove_tag(conversation, tag)
    logger.info("Removed tag_id=%s from conversation_id=%s.", tag_id, conversation_id)
    return {"message": "Tag removed from conversation successfully"}


def _get_conversation(conversation_id: int, db: Session) -> Conversation:
    """Load a conversation for tag operations or raise a 404 response."""
    conversation = ConversationRepository(db).get_by_id(conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation
