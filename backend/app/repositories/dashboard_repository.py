"""SQLAlchemy repository for Project dashboard data aggregation."""

from sqlalchemy.orm import Session

from app.models.conversation import Conversation
from app.models.decision import Decision
from app.models.knowledge import Knowledge
from app.models.message import Message
from app.models.project import Project
from app.models.research import Research
from app.models.task import Task
from app.models.timeline import Timeline


class DashboardRepository:
    """Provide database reads required by project dashboard services."""

    def __init__(self, db: Session) -> None:
        """Initialize the repository with an injected SQLAlchemy session."""
        self.db = db

    def get_project(self, project_id: int) -> Project | None:
        """Return a project by ID when it exists."""
        return self.db.query(Project).filter(Project.id == project_id).first()

    def count_project_conversations(self, project_id: int) -> int:
        """Count all conversations, including archived conversations."""
        return self.db.query(Conversation).filter(
            Conversation.project_id == project_id
        ).count()

    def count_project_messages(self, project_id: int) -> int:
        """Count messages belonging to conversations in one project."""
        return self.db.query(Message).join(Conversation).filter(
            Conversation.project_id == project_id
        ).count()

    def count_project_records(self, model: type, project_id: int) -> int:
        """Count project-scoped records for a specialized model."""
        return self.db.query(model).filter(model.project_id == project_id).count()

    def get_recent_conversations(
        self,
        project_id: int,
        limit: int = 10,
    ) -> list[Conversation]:
        """Return recent non-archived conversations for a project."""
        return self.db.query(Conversation).filter(
            Conversation.project_id == project_id,
            Conversation.is_archived.is_(False),
        ).order_by(Conversation.updated_at.desc()).limit(limit).all()

    def get_pinned_conversations(self, project_id: int) -> list[Conversation]:
        """Return pinned non-archived conversations for a project."""
        return self.db.query(Conversation).filter(
            Conversation.project_id == project_id,
            Conversation.is_archived.is_(False),
            Conversation.is_pinned.is_(True),
        ).order_by(Conversation.updated_at.desc()).all()

    def memory_counts(self, project_id: int) -> dict[str, int]:
        """Return counts for specialized memory storage tables."""
        return {
            "decisions": self.count_project_records(Decision, project_id),
            "knowledge": self.count_project_records(Knowledge, project_id),
            "research": self.count_project_records(Research, project_id),
            "tasks": self.count_project_records(Task, project_id),
            "timeline": self.count_project_records(Timeline, project_id),
        }
