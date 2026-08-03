"""SQLAlchemy repository for Context and Memory Engine persistence."""

from datetime import datetime
from typing import TypeAlias

from sqlalchemy.orm import Session

from app.memory.memory import Memory
from app.models.decision import Decision
from app.models.knowledge import Knowledge
from app.models.research import Research
from app.models.task import Task
from app.models.timeline import Timeline

StoredMemory: TypeAlias = Decision | Knowledge | Research | Task | Timeline


class MemoryRepository:
    """Persist and query memory records through specialized SQLAlchemy models.

    This repository owns database access only. It does not extract, classify,
    or score memories; those responsibilities belong to the memory pipeline.
    """

    CATEGORY_MODELS = {
        "decision": Decision,
        "knowledge": Knowledge,
        "research": Research,
        "task": Task,
        "timeline": Timeline,
    }
    MEMORY_MODELS = tuple(CATEGORY_MODELS.values())

    def __init__(self, db: Session) -> None:
        """Initialize the repository with an injected SQLAlchemy session."""
        self.db = db

    def save_memory(self, memory: Memory) -> StoredMemory | None:
        """Persist one classified memory and return its database record.

        General memories are intentionally not persisted in the current
        version because they do not map to a specialized database table.
        """
        database_record = self._build_record(memory)

        if database_record is None:
            return None

        self.db.add(database_record)
        self.db.commit()
        self.db.refresh(database_record)

        return database_record

    def save_memories(self, memories: list[Memory]) -> list[StoredMemory]:
        """Persist multiple classified memories in one transaction."""
        database_records = [
            record
            for memory in memories
            if (record := self._build_record(memory)) is not None
        ]

        if not database_records:
            return []

        self.db.add_all(database_records)
        self.db.commit()

        for database_record in database_records:
            self.db.refresh(database_record)

        return database_records

    def get_memory(self, memory_id: int) -> StoredMemory | None:
        """Return the first specialized memory record matching an ID.

        Specialized tables have independent primary-key sequences. Callers
        that need an unambiguous lookup should retain the record category.
        """
        for model in self.MEMORY_MODELS:
            database_record = self.db.query(model).filter(
                model.id == memory_id
            ).first()

            if database_record is not None:
                return database_record

        return None

    def get_project_memories(self, project_id: int) -> list[StoredMemory]:
        """Return all specialized memory records associated with a project."""
        return [
            database_record
            for model in self.MEMORY_MODELS
            for database_record in self.db.query(model)
            .filter(model.project_id == project_id)
            .all()
        ]

    def get_memories_by_category(
        self,
        project_id: int,
        category: str,
    ) -> list[StoredMemory]:
        """Return project memories from the specialized table for category."""
        model = self.CATEGORY_MODELS.get(category.casefold())

        if model is None:
            return []

        return self.db.query(model).filter(
            model.project_id == project_id
        ).all()

    def get_recent_memories(
        self,
        project_id: int,
        limit: int = 20,
    ) -> list[StoredMemory]:
        """Return the newest available project memory records up to limit.

        Only Knowledge and Timeline records currently include timestamps.
        Records without a timestamp sort after those dated records.
        """
        memories = self.get_project_memories(project_id)
        memories.sort(
            key=lambda memory: getattr(memory, "created_at", None)
            or datetime.min,
            reverse=True,
        )
        return memories[:limit]

    def get_important_memories(
        self,
        project_id: int,
        min_importance: float = 0.7,
    ) -> list[StoredMemory]:
        """Return project records with an explicit importance threshold."""
        decisions = self.db.query(Decision).filter(
            Decision.project_id == project_id,
            Decision.importance >= min_importance,
        ).all()
        knowledge = self.db.query(Knowledge).filter(
            Knowledge.project_id == project_id,
            Knowledge.importance >= min_importance,
        ).all()

        return [*decisions, *knowledge]

    def _build_record(self, memory: Memory) -> StoredMemory | None:
        """Map a classified internal memory to its specialized ORM model."""
        if memory.category == "decision":
            return Decision(
                content=memory.content,
                importance=memory.importance,
                project_id=memory.project_id,
            )
        if memory.category == "knowledge":
            return Knowledge(
                title=self._title_from_content(memory.content, 200),
                content=memory.content,
                category=memory.category,
                importance=memory.importance,
                project_id=memory.project_id,
            )
        if memory.category == "research":
            return Research(
                title=self._title_from_content(memory.content, 200),
                content=memory.content,
                source=memory.source,
                project_id=memory.project_id,
            )
        if memory.category == "task":
            return Task(
                title=self._title_from_content(memory.content, 150),
                description=memory.content,
                project_id=memory.project_id,
            )
        if memory.category == "timeline":
            return Timeline(
                event=self._title_from_content(memory.content, 200),
                description=memory.content,
                project_id=memory.project_id,
            )

        return None

    @staticmethod
    def _title_from_content(content: str, max_length: int) -> str:
        """Create a table-compatible title or event from memory content."""
        return content[:max_length]
