"""Unit tests for Knowledge, Research, and Timeline schema validation."""

import pytest
from pydantic import ValidationError

from app.schemas.knowledge import KnowledgeCreate
from app.schemas.research import ResearchCreate
from app.schemas.timeline import TimelineCreate


def test_research_trims_optional_source_and_accepts_boundaries() -> None:
    """Research fields are stripped and source remains optional."""
    research = ResearchCreate(
        title=f"  {'t' * 200}  ",
        content=f"  {'c' * 10000}  ",
        source="  https://example.test  ",
        project_id=1,
    )

    assert research.title == "t" * 200
    assert research.content == "c" * 10000
    assert research.source == "https://example.test"
    assert ResearchCreate(title="abc", content="valid", project_id=1).source is None


@pytest.mark.parametrize(
    ("payload", "field"),
    [
        ({"title": "ab", "content": "valid", "project_id": 1}, "title"),
        ({"title": "valid", "content": "abcd", "project_id": 1}, "content"),
        ({"title": "valid", "content": "valid", "source": "s" * 501, "project_id": 1}, "source"),
        ({"title": "valid", "content": "valid", "project_id": 0}, "project_id"),
        ({"title": "valid", "project_id": 1}, "content"),
    ],
)
def test_research_rejects_invalid_or_missing_fields(
    payload: dict[str, object],
    field: str,
) -> None:
    """Research schema applies required, length, and positive-ID constraints."""
    with pytest.raises(ValidationError) as error:
        ResearchCreate(**payload)

    assert field in str(error.value)


def test_timeline_trims_text_and_accepts_exact_boundaries() -> None:
    """Timeline text is trimmed before validation at supported limits."""
    timeline = TimelineCreate(
        event=f"  {'e' * 200}  ",
        description=f"  {'d' * 1000}  ",
        project_id=1,
    )

    assert timeline.event == "e" * 200
    assert timeline.description == "d" * 1000


@pytest.mark.parametrize(
    ("payload", "field"),
    [
        ({"event": "ab", "description": "valid", "project_id": 1}, "event"),
        ({"event": "valid", "description": "abcd", "project_id": 1}, "description"),
        ({"event": "valid", "description": "valid", "project_id": -1}, "project_id"),
        ({"event": "valid", "description": "valid"}, "project_id"),
    ],
)
def test_timeline_rejects_invalid_or_missing_fields(
    payload: dict[str, object],
    field: str,
) -> None:
    """Timeline schema rejects invalid boundaries and missing required data."""
    with pytest.raises(ValidationError) as error:
        TimelineCreate(**payload)

    assert field in str(error.value)


def test_knowledge_trims_fields_and_defaults_importance() -> None:
    """Knowledge accepts declared boundaries and defaults importance to one."""
    knowledge = KnowledgeCreate(
        title="  abc  ",
        content="  valid content  ",
        category="  AI  ",
        project_id=1,
    )

    assert knowledge.title == "abc"
    assert knowledge.content == "valid content"
    assert knowledge.category == "AI"
    assert knowledge.importance == 1


@pytest.mark.parametrize(
    ("payload", "field"),
    [
        ({"title": "ab", "content": "valid", "category": "AI", "project_id": 1}, "title"),
        ({"title": "valid", "content": "abcd", "category": "AI", "project_id": 1}, "content"),
        ({"title": "valid", "content": "valid", "category": "A", "project_id": 1}, "category"),
        ({"title": "valid", "content": "valid", "category": "AI", "importance": 0, "project_id": 1}, "importance"),
        ({"title": "valid", "content": "valid", "category": "AI", "project_id": 0}, "project_id"),
        ({"title": "valid", "content": "valid", "project_id": 1}, "category"),
    ],
)
def test_knowledge_rejects_invalid_or_missing_fields(
    payload: dict[str, object],
    field: str,
) -> None:
    """Knowledge schema enforces text, importance, and project constraints."""
    with pytest.raises(ValidationError) as error:
        KnowledgeCreate(**payload)

    assert field in str(error.value)
