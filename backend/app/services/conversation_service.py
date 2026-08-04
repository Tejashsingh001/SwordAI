"""Application service functions for Conversation CRUD operations."""

import logging
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository
from app.schemas.conversation import ConversationCreate

logger = logging.getLogger(__name__)

SUMMARY_MAX_LENGTH = 150
SUMMARY_MESSAGE_LIMIT = 3


def create_conversation(
    conversation: ConversationCreate,
    db: Session,
    first_message: str | None = None,
) -> Conversation:
    """Create and return a project conversation."""
    repository = ConversationRepository(db)
    title = conversation.title or _generate_conversation_title(first_message)
    summary = conversation.summary or ""
    summary_is_manual = conversation.summary is not None
    return repository.create(
        conversation.project_id,
        title,
        summary,
        summary_is_manual,
        conversation.is_pinned or False,
        conversation.is_archived or False,
    )


def get_conversations(
    db: Session,
    include_archived: bool = False,
) -> list[Conversation]:
    """Return conversations, excluding archived records by default."""
    conversations = ConversationRepository(db).get_all()
    if not include_archived:
        conversations = [
            conversation
            for conversation in conversations
            if not conversation.is_archived
        ]
    return _sort_conversations(conversations)


def search_conversations(
    project_id: int,
    query: str | None,
    db: Session,
    include_archived: bool = False,
    tag: str | None = None,
) -> list[Conversation]:
    """Return project conversations matching title, summary, or tags.

    Matching is deterministic, case-insensitive, and ignores surrounding
    whitespace. An empty query returns all conversations for the project.
    """
    normalized_query = (query or "").strip().casefold()
    normalized_tag = (tag or "").strip().casefold()
    conversations = ConversationRepository(db).get_by_project_id(project_id)

    if not include_archived:
        conversations = [
            conversation
            for conversation in conversations
            if not conversation.is_archived
        ]

    if normalized_query:
        conversations = [
            conversation
            for conversation in conversations
            if normalized_query in conversation.title.casefold()
            or normalized_query in (conversation.summary or "").casefold()
            or any(
                normalized_query in tag_record.name.casefold()
                for tag_record in conversation.tags
            )
        ]

    if normalized_tag:
        conversations = [
            conversation
            for conversation in conversations
            if any(
                normalized_tag in tag_record.name.casefold()
                for tag_record in conversation.tags
            )
        ]

    conversations = _sort_conversations(conversations)
    logger.info(
        "Conversation search returned %s results for project_id=%s.",
        len(conversations),
        project_id,
    )
    return conversations


def get_conversation(conversation_id: int, db: Session) -> Conversation:
    """Return one conversation or raise the existing-style 404 response."""
    conversation = ConversationRepository(db).get_by_id(conversation_id)

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    return conversation


def update_conversation(
    conversation_id: int,
    conversation: ConversationCreate,
    db: Session,
) -> Conversation:
    """Update and return one conversation or raise a 404 response."""
    repository = ConversationRepository(db)
    db_conversation = repository.get_by_id(conversation_id)

    if db_conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    title = conversation.title or db_conversation.title
    summary = db_conversation.summary
    summary_is_manual = db_conversation.summary_is_manual
    is_pinned = (
        conversation.is_pinned
        if conversation.is_pinned is not None
        else db_conversation.is_pinned
    )
    is_archived = (
        conversation.is_archived
        if conversation.is_archived is not None
        else db_conversation.is_archived
    )

    if conversation.summary is not None:
        summary = conversation.summary
        summary_is_manual = True

    return repository.update(
        db_conversation,
        conversation.project_id,
        title,
        summary,
        summary_is_manual,
        is_pinned,
        is_archived,
    )


def delete_conversation(conversation_id: int, db: Session) -> dict[str, str]:
    """Delete one conversation or raise a 404 response."""
    repository = ConversationRepository(db)
    db_conversation = repository.get_by_id(conversation_id)

    if db_conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    repository.delete(db_conversation)
    return {"message": "Conversation deleted successfully"}


def pin_conversation(conversation_id: int, db: Session) -> Conversation:
    """Mark one conversation as pinned or raise a 404 response."""
    return _set_conversation_pinned(conversation_id, True, db)


def unpin_conversation(conversation_id: int, db: Session) -> Conversation:
    """Mark one conversation as unpinned or raise a 404 response."""
    return _set_conversation_pinned(conversation_id, False, db)


def archive_conversation(conversation_id: int, db: Session) -> Conversation:
    """Archive one conversation or raise a 404 response."""
    return _set_conversation_archived(conversation_id, True, db)


def restore_conversation(conversation_id: int, db: Session) -> Conversation:
    """Restore one archived conversation or raise a 404 response."""
    return _set_conversation_archived(conversation_id, False, db)


def _set_conversation_pinned(
    conversation_id: int,
    is_pinned: bool,
    db: Session,
) -> Conversation:
    """Persist a conversation pin-state change through the repository."""
    repository = ConversationRepository(db)
    conversation = repository.get_by_id(conversation_id)

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    logger.info(
        "Set is_pinned=%s for conversation_id=%s.",
        is_pinned,
        conversation_id,
    )
    return repository.set_pinned(conversation, is_pinned)


def _set_conversation_archived(
    conversation_id: int,
    is_archived: bool,
    db: Session,
) -> Conversation:
    """Persist a conversation archive-state change through the repository."""
    repository = ConversationRepository(db)
    conversation = repository.get_by_id(conversation_id)

    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")

    logger.info(
        "Set is_archived=%s for conversation_id=%s.",
        is_archived,
        conversation_id,
    )
    return repository.set_archived(conversation, is_archived)


def refresh_conversation_summary(
    conversation_id: int,
    db: Session,
) -> Conversation:
    """Generate and persist a summary unless one was manually assigned."""
    repository = ConversationRepository(db)
    conversation = repository.get_by_id(conversation_id)

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found",
        )

    if conversation.summary_is_manual:
        logger.info(
            "Skipping automatic summary for conversation_id=%s.",
            conversation_id,
        )
        return conversation

    messages = MessageRepository(db).get_user_messages_by_conversation_id(
        conversation_id
    )
    summary = _generate_conversation_summary(
        [message.content for message in messages]
    )
    logger.info(
        "Generated automatic summary for conversation_id=%s.",
        conversation_id,
    )
    return repository.update_summary(conversation, summary)


def _generate_conversation_title(first_message: str | None) -> str:
    """Create a deterministic, word-safe title from a first user message.

    Whitespace is normalized before truncation. When a title exceeds 60
    characters, the nearest preceding word boundary is preferred; a long
    unbroken word is truncated only when no boundary is available.
    """
    normalized_message = " ".join((first_message or "").split())

    if not normalized_message:
        return "New Conversation"

    if len(normalized_message) <= 60:
        return normalized_message

    truncated_title = normalized_message[:60]
    word_boundary = truncated_title.rfind(" ")

    if word_boundary > 0:
        return truncated_title[:word_boundary]

    return truncated_title


def _generate_conversation_summary(user_messages: list[str]) -> str:
    """Build a readable, word-safe summary from early user messages."""
    meaningful_messages = [
        " ".join(message.split())
        for message in user_messages
        if message and message.strip()
    ]
    summary = " ".join(meaningful_messages[:SUMMARY_MESSAGE_LIMIT])

    if len(summary) <= SUMMARY_MAX_LENGTH:
        return summary

    truncated_summary = summary[:SUMMARY_MAX_LENGTH]
    word_boundary = truncated_summary.rfind(" ")

    if word_boundary > 0:
        return truncated_summary[:word_boundary]

    return truncated_summary


def _sort_conversations(
    conversations: list[Conversation],
) -> list[Conversation]:
    """Order pinned records first and newest records within each group."""
    return sorted(
        conversations,
        key=lambda conversation: (
            conversation.is_pinned,
            conversation.updated_at or datetime.min,
        ),
        reverse=True,
    )
