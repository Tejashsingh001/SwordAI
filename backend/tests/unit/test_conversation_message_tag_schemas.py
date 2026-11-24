"""Unit tests for Conversation, Message, Tag, and dashboard schemas."""

from datetime import datetime

import pytest
from pydantic import ValidationError

from app.schemas.conversation import ConversationCreate
from app.schemas.dashboard import ConversationStatsResponse, ProjectDashboardResponse
from app.schemas.message import MessageCreate
from app.schemas.tag import TagCreate


def test_conversation_trims_optional_text_and_defaults_to_none() -> None:
    """Conversation optional text normalizes whitespace-only values to None."""
    conversation = ConversationCreate(
        project_id=1,
        title="  Planning  ",
        summary="   ",
    )

    assert conversation.title == "Planning"
    assert conversation.summary is None
    assert conversation.is_pinned is None
    assert conversation.is_archived is None


@pytest.mark.parametrize(
    ("payload", "field"),
    [
        ({"project_id": 0}, "project_id"),
        ({"project_id": 1, "title": "t" * 201}, "title"),
        ({"project_id": 1, "summary": "s" * 501}, "summary"),
        ({}, "project_id"),
    ],
)
def test_conversation_rejects_invalid_or_missing_fields(
    payload: dict[str, object],
    field: str,
) -> None:
    """Conversation schema enforces project ID and optional text maxima."""
    with pytest.raises(ValidationError) as error:
        ConversationCreate(**payload)

    assert field in str(error.value)


def test_message_trims_content_and_accepts_exact_upper_boundary() -> None:
    """Message content is stripped before its declared length check."""
    message = MessageCreate(
        conversation_id=1,
        role="user",
        content=f"  {'m' * 10000}  ",
    )

    assert message.content == "m" * 10000


@pytest.mark.parametrize(
    ("payload", "field"),
    [
        ({"conversation_id": 0, "role": "user", "content": "text"}, "conversation_id"),
        ({"conversation_id": 1, "role": "system", "content": "text"}, "role"),
        ({"conversation_id": 1, "role": "user", "content": "   "}, "content"),
        ({"conversation_id": 1, "role": "user", "content": "m" * 10001}, "content"),
        ({"conversation_id": 1, "content": "text"}, "role"),
    ],
)
def test_message_rejects_invalid_or_missing_fields(
    payload: dict[str, object],
    field: str,
) -> None:
    """Message schema enforces author role, content, and ownership fields."""
    with pytest.raises(ValidationError) as error:
        MessageCreate(**payload)

    assert field in str(error.value)


def test_tag_trims_name_and_accepts_declared_boundaries() -> None:
    """Tag names are stripped before applying the two-to-fifty limit."""
    tag = TagCreate(name=f"  {'t' * 50}  ")

    assert tag.name == "t" * 50


@pytest.mark.parametrize("name", ["a", "t" * 51, "   "])
def test_tag_rejects_invalid_names(name: str) -> None:
    """Tag names must remain within the configured range after trimming."""
    with pytest.raises(ValidationError):
        TagCreate(name=name)


def test_dashboard_schemas_accept_nested_response_data() -> None:
    """Dashboard response schemas parse their required aggregate structure."""
    timestamp = datetime(2026, 1, 1)
    conversation = {
        "id": 1,
        "project_id": 1,
        "title": "Conversation",
        "summary": "Summary",
        "is_pinned": False,
        "is_archived": False,
        "tags": [{"id": 1, "name": "AI"}],
        "created_at": timestamp,
        "updated_at": timestamp,
    }
    stats = ConversationStatsResponse(
        total_messages=2,
        user_messages=1,
        assistant_messages=1,
        created_at=timestamp,
        updated_at=timestamp,
        is_pinned=False,
        is_archived=False,
        tags=conversation["tags"],
    )
    dashboard = ProjectDashboardResponse(
        total_conversations=1,
        total_messages=2,
        total_memories=0,
        total_decisions=0,
        total_knowledge=0,
        total_research=0,
        total_tasks=0,
        recent_conversations=[conversation],
        pinned_conversations=[],
    )

    assert stats.tags[0].name == "AI"
    assert dashboard.recent_conversations[0].title == "Conversation"
