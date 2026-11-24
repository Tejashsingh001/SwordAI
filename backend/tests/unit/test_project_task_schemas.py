"""Unit tests for Project and Task Pydantic schema validation."""

import pytest
from pydantic import ValidationError

from app.schemas.project import ProjectCreate
from app.schemas.task import TaskCreate


def test_project_accepts_boundary_values_and_strips_whitespace() -> None:
    """Project fields are trimmed before their declared length checks."""
    project = ProjectCreate(name="  abc  ", description=f"  {'d' * 1000}  ")

    assert project.name == "abc"
    assert project.description == "d" * 1000


@pytest.mark.parametrize(
    ("payload", "field"),
    [
        ({"name": "ab", "description": "valid"}, "name"),
        ({"name": "n" * 101, "description": "valid"}, "name"),
        ({"name": "valid", "description": "abcd"}, "description"),
        ({"name": "valid", "description": "d" * 1001}, "description"),
        ({"name": "valid"}, "description"),
    ],
)
def test_project_rejects_invalid_or_missing_fields(
    payload: dict[str, str],
    field: str,
) -> None:
    """Project schema enforces required fields and declared bounds."""
    with pytest.raises(ValidationError) as error:
        ProjectCreate(**payload)

    assert field in str(error.value)


def test_task_uses_default_status_and_accepts_allowed_statuses() -> None:
    """Task status defaults to Pending and accepts only declared literals."""
    default_task = TaskCreate(
        title="Ship tests",
        description="Add focused schema tests.",
        project_id=1,
    )

    assert default_task.status == "Pending"

    for status in ("Pending", "In Progress", "Completed"):
        task = TaskCreate(
            title="t" * 150,
            description="d" * 1000,
            status=status,
            project_id=1,
        )
        assert task.status == status


@pytest.mark.parametrize(
    ("payload", "field"),
    [
        (
            {"title": "ab", "description": "valid", "project_id": 1},
            "title",
        ),
        (
            {"title": "t" * 151, "description": "valid", "project_id": 1},
            "title",
        ),
        (
            {"title": "valid", "description": "abcd", "project_id": 1},
            "description",
        ),
        (
            {"title": "valid", "description": "d" * 1001, "project_id": 1},
            "description",
        ),
        (
            {"title": "valid", "description": "valid", "status": "Done", "project_id": 1},
            "status",
        ),
        (
            {"title": "valid", "description": "valid", "project_id": 0},
            "project_id",
        ),
        ({"title": "valid", "description": "valid"}, "project_id"),
    ],
)
def test_task_rejects_invalid_or_missing_fields(
    payload: dict[str, object],
    field: str,
) -> None:
    """Task schema applies title, description, status, and ID validation."""
    with pytest.raises(ValidationError) as error:
        TaskCreate(**payload)

    assert field in str(error.value)
