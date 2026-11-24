"""Unit tests for core services that currently use SQLAlchemy directly."""

import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.knowledge import KnowledgeCreate
from app.schemas.project import ProjectCreate
from app.schemas.research import ResearchCreate
from app.schemas.task import TaskCreate
from app.schemas.timeline import TimelineCreate
from app.services import (
    knowledge_service,
    project_service,
    research_service,
    task_service,
    timeline_service,
)


def test_project_service_crud_and_missing_update(db_session: Session) -> None:
    """Project service persists CRUD changes and returns its 404 behavior."""
    project = project_service.create_project(ProjectCreate(name="Project", description="Initial project"), db_session)
    assert project_service.get_projects(db_session) == [project]
    assert project_service.update_project(project.id, ProjectCreate(name="Updated", description="Updated project"), db_session).name == "Updated"
    assert project_service.delete_project(project.id, db_session) == {"message": "Project deleted successfully"}

    with pytest.raises(HTTPException) as error:
        project_service.update_project(999, ProjectCreate(name="Updated", description="Updated project"), db_session)
    assert error.value.status_code == 404


def test_task_service_crud_and_missing_delete(db_session: Session) -> None:
    """Task service persists CRUD data and reports missing records."""
    task = task_service.create_task(TaskCreate(title="Task", description="Initial task", project_id=1), db_session)
    assert task_service.get_tasks(db_session) == [task]
    assert task_service.update_task(task.id, TaskCreate(title="Updated", description="Updated task", status="Completed", project_id=2), db_session).status == "Completed"
    assert task_service.delete_task(task.id, db_session) == {"message": "Task deleted successfully"}

    with pytest.raises(HTTPException) as error:
        task_service.delete_task(999, db_session)
    assert error.value.status_code == 404


def test_knowledge_service_crud_and_missing_get_behavior(db_session: Session) -> None:
    """Knowledge service persists fields and returns a 404 when updating a missing row."""
    knowledge = knowledge_service.create_knowledge(KnowledgeCreate(title="Knowledge", content="Initial knowledge", category="AI", project_id=1), db_session)
    assert knowledge_service.get_knowledge(db_session) == [knowledge]
    updated = knowledge_service.update_knowledge(knowledge.id, KnowledgeCreate(title="Updated", content="Updated knowledge", category="API", importance=3, project_id=2), db_session)
    assert (updated.category, updated.importance, updated.project_id) == ("API", 3, 2)
    assert knowledge_service.delete_knowledge(knowledge.id, db_session) == {"message": "Knowledge deleted successfully"}

    with pytest.raises(HTTPException) as error:
        knowledge_service.update_knowledge(999, KnowledgeCreate(title="Updated", content="Updated knowledge", category="API", project_id=1), db_session)
    assert error.value.status_code == 404


def test_research_service_crud_and_missing_delete(db_session: Session) -> None:
    """Research service persists CRUD data and reports a missing deletion."""
    research = research_service.create_research(ResearchCreate(title="Research", content="Initial research", source="Source", project_id=1), db_session)
    assert research_service.get_research(db_session) == [research]
    assert research_service.update_research(research.id, ResearchCreate(title="Updated", content="Updated research", project_id=2), db_session).project_id == 2
    assert research_service.delete_research(research.id, db_session) == {"message": "Research deleted successfully"}

    with pytest.raises(HTTPException) as error:
        research_service.delete_research(999, db_session)
    assert error.value.status_code == 404


def test_timeline_service_crud_and_missing_update(db_session: Session) -> None:
    """Timeline service persists CRUD changes and reports missing updates."""
    timeline = timeline_service.create_timeline(TimelineCreate(event="Created", description="Initial event", project_id=1), db_session)
    assert timeline_service.get_timeline(db_session) == [timeline]
    assert timeline_service.update_timeline(timeline.id, TimelineCreate(event="Updated", description="Updated event", project_id=2), db_session).event == "Updated"
    assert timeline_service.delete_timeline(timeline.id, db_session) == {"message": "Timeline event deleted successfully"}

    with pytest.raises(HTTPException) as error:
        timeline_service.update_timeline(999, TimelineCreate(event="Updated", description="Updated event", project_id=1), db_session)
    assert error.value.status_code == 404
