"""Persistence-focused unit tests for implemented conversation repositories."""

from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.models.project import Project
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository
from app.repositories.tag_repository import TagRepository


def _project(db_session: Session) -> Project:
    project = Project(name="Repository project", description="Repository tests")
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)
    return project


def test_conversation_repository_crud_and_missing_lookup(db_session: Session) -> None:
    """Conversation repository persists, updates, deletes, and misses cleanly."""
    repository = ConversationRepository(db_session)
    project = _project(db_session)
    conversation = repository.create(project.id, "Initial", "Summary", False, False, False)

    assert repository.get_by_id(conversation.id) is conversation
    assert repository.get_by_id(999) is None
    assert repository.get_by_project_id(project.id) == [conversation]

    updated = repository.update(
        conversation,
        project.id,
        "Updated",
        "Manual summary",
        True,
        True,
        True,
    )
    assert (updated.title, updated.summary, updated.summary_is_manual) == (
        "Updated",
        "Manual summary",
        True,
    )
    assert updated.is_pinned is True
    assert updated.is_archived is True

    repository.delete(updated)
    assert repository.get_by_id(conversation.id) is None


def test_conversation_repository_updates_state_and_tag_relationships(
    db_session: Session,
) -> None:
    """Pin/archive/summary operations and tag links persist through the repository."""
    conversations = ConversationRepository(db_session)
    tags = TagRepository(db_session)
    conversation = conversations.create(_project(db_session).id, "Chat", "", False, False, False)
    tag = tags.create("Architecture")

    assert conversations.set_pinned(conversation, True).is_pinned is True
    assert conversations.set_archived(conversation, True).is_archived is True
    assert conversations.update_summary(conversation, "Generated").summary == "Generated"

    conversations.add_tag(conversation, tag)
    conversations.add_tag(conversation, tag)
    assert [assigned.name for assigned in conversation.tags] == ["Architecture"]

    conversations.remove_tag(conversation, tag)
    conversations.remove_tag(conversation, tag)
    assert conversation.tags == []


def test_message_repository_crud_filters_ordering_and_counts(db_session: Session) -> None:
    """Message repository filters by conversation, sorts chronologically, and counts roles."""
    conversation = ConversationRepository(db_session).create(
        _project(db_session).id,
        "Chat",
        "",
        False,
        False,
        False,
    )
    repository = MessageRepository(db_session)
    first = repository.create(conversation.id, "user", "First")
    second = repository.create(conversation.id, "assistant", "Second")
    first.created_at = (
        datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(minutes=1)
    )
    db_session.commit()

    assert repository.get_by_id(999) is None
    assert [message.content for message in repository.get_by_conversation_id(conversation.id)] == [
        "First",
        "Second",
    ]
    assert repository.get_user_messages_by_conversation_id(conversation.id) == [first]
    assert repository.count_by_conversation_id(conversation.id) == 2
    assert repository.count_by_conversation_and_role(conversation.id, "assistant") == 1

    updated = repository.update(second, conversation.id, "assistant", "Updated")
    assert updated.content == "Updated"
    repository.delete(first)
    assert repository.get_by_id(first.id) is None


def test_tag_repository_crud_and_case_insensitive_lookup(db_session: Session) -> None:
    """Tag repository supports CRUD and case-insensitive exact-name lookup."""
    repository = TagRepository(db_session)
    tag = repository.create("Backend")

    assert repository.get_by_id(tag.id) is tag
    assert repository.get_by_id(999) is None
    assert repository.get_by_name("backend") is tag
    assert repository.get_by_name("missing") is None
    assert repository.update(tag, "API").name == "API"
    assert repository.get_all() == [tag]

    repository.delete(tag)
    assert repository.get_by_id(tag.id) is None
