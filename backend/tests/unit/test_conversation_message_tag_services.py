"""Unit tests for implemented conversation, message, and tag services."""

from fastapi import HTTPException
import pytest
from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.conversation import ConversationCreate
from app.schemas.message import MessageCreate
from app.schemas.tag import TagCreate
from app.services import conversation_service, message_service, tag_service


def _project(db_session: Session) -> Project:
    project = Project(name="Service project", description="Service layer tests")
    db_session.add(project)
    db_session.commit()
    db_session.refresh(project)
    return project


def test_conversation_service_generates_title_and_filters_archived_records(
    db_session: Session,
) -> None:
    """Conversation creation derives a title and hides archived conversations by default."""
    project = _project(db_session)
    conversation = conversation_service.create_conversation(
        ConversationCreate(project_id=project.id),
        db_session,
        first_message="  Build the context memory engine for SwordAI  ",
    )

    assert conversation.title == "Build the context memory engine for SwordAI"
    assert conversation_service.get_conversations(db_session) == [conversation]

    conversation_service.archive_conversation(conversation.id, db_session)
    assert conversation_service.get_conversations(db_session) == []
    assert conversation_service.get_conversations(db_session, include_archived=True) == [conversation]
    assert conversation_service.restore_conversation(conversation.id, db_session).is_archived is False


def test_conversation_service_searches_and_orders_pinned_records(
    db_session: Session,
) -> None:
    """Search matches title, summary, and tags and returns pinned records first."""
    project = _project(db_session)
    first = conversation_service.create_conversation(
        ConversationCreate(project_id=project.id, title="Backend planning", summary="API work"),
        db_session,
    )
    second = conversation_service.create_conversation(
        ConversationCreate(project_id=project.id, title="Other chat"),
        db_session,
    )
    tag = tag_service.create_tag(TagCreate(name="Memory"), db_session)
    tag_service.add_tag_to_conversation(second.id, tag.id, db_session)
    conversation_service.pin_conversation(second.id, db_session)

    assert conversation_service.get_conversations(db_session)[0].id == second.id
    assert conversation_service.search_conversations(project.id, "api", db_session) == [first]
    assert conversation_service.search_conversations(project.id, "memory", db_session) == [second]
    assert conversation_service.search_conversations(project.id, "", db_session, tag="memory") == [second]


def test_conversation_service_updates_summary_and_reports_missing_records(
    db_session: Session,
) -> None:
    """Updates preserve values as implemented and missing records return 404 errors."""
    project = _project(db_session)
    conversation = conversation_service.create_conversation(
        ConversationCreate(project_id=project.id, title="Original"),
        db_session,
    )
    updated = conversation_service.update_conversation(
        conversation.id,
        ConversationCreate(project_id=project.id, summary="Manual summary", is_pinned=True),
        db_session,
    )

    assert updated.title == "Original"
    assert updated.summary == "Manual summary"
    assert updated.summary_is_manual is True
    assert updated.is_pinned is True

    for operation in (
        lambda: conversation_service.get_conversation(999, db_session),
        lambda: conversation_service.update_conversation(999, ConversationCreate(project_id=project.id), db_session),
        lambda: conversation_service.delete_conversation(999, db_session),
        lambda: conversation_service.pin_conversation(999, db_session),
    ):
        with pytest.raises(HTTPException) as error:
            operation()
        assert error.value.status_code == 404


def test_message_service_refreshes_automatic_summary_for_user_messages(
    db_session: Session,
) -> None:
    """User messages refresh automatic summaries; assistant messages do not replace them."""
    project = _project(db_session)
    conversation = conversation_service.create_conversation(
        ConversationCreate(project_id=project.id),
        db_session,
    )
    user_message = message_service.create_message(
        MessageCreate(conversation_id=conversation.id, role="user", content="  First useful message  "),
        db_session,
    )
    message_service.create_message(
        MessageCreate(conversation_id=conversation.id, role="assistant", content="Response"),
        db_session,
    )

    refreshed = conversation_service.get_conversation(conversation.id, db_session)
    assert user_message.content == "First useful message"
    assert refreshed.summary == "First useful message"
    assert [message.role for message in message_service.get_conversation_messages(conversation.id, db_session)] == [
        "user",
        "assistant",
    ]

    assert message_service.delete_message(user_message.id, db_session) == {
        "message": "Message deleted successfully"
    }
    assert conversation_service.get_conversation(conversation.id, db_session).summary == ""


def test_message_and_tag_services_handle_crud_and_missing_records(
    db_session: Session,
) -> None:
    """Message and tag services persist CRUD results and expose their 404/409 behavior."""
    project = _project(db_session)
    conversation = conversation_service.create_conversation(
        ConversationCreate(project_id=project.id),
        db_session,
    )
    message = message_service.create_message(
        MessageCreate(conversation_id=conversation.id, role="assistant", content="Initial"),
        db_session,
    )
    updated_message = message_service.update_message(
        message.id,
        MessageCreate(conversation_id=conversation.id, role="assistant", content="Updated"),
        db_session,
    )
    tag = tag_service.create_tag(TagCreate(name="Backend"), db_session)

    assert updated_message.content == "Updated"
    assert message_service.get_message(message.id, db_session).content == "Updated"
    assert tag_service.update_tag(tag.id, TagCreate(name="API"), db_session).name == "API"
    assert tag_service.add_tag_to_conversation(conversation.id, tag.id, db_session).id == tag.id
    assert [assigned.name for assigned in tag_service.get_conversation_tags(conversation.id, db_session)] == ["API"]
    assert tag_service.remove_tag_from_conversation(conversation.id, tag.id, db_session) == {
        "message": "Tag removed from conversation successfully"
    }

    with pytest.raises(HTTPException) as duplicate_error:
        tag_service.create_tag(TagCreate(name="api"), db_session)
    assert duplicate_error.value.status_code == 409

    with pytest.raises(HTTPException) as missing_error:
        message_service.get_message(999, db_session)
    assert missing_error.value.status_code == 404
