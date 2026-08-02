"""Persistence pipeline for extracted, classified, and scored memories."""

from sqlalchemy.orm import Session

from app.memory.classifier import MemoryClassifier
from app.memory.extractor import MemoryExtractor
from app.memory.importance import MemoryImportance
from app.memory.memory import Memory
from app.models.decision import Decision
from app.models.knowledge import Knowledge
from app.models.research import Research
from app.models.task import Task
from app.models.timeline import Timeline


class MemoryStorage:
    """Coordinate the memory pipeline and persist specialized records.

    Memories are routed to specialized database tables after extraction,
    classification, and importance scoring. General memories are intentionally
    ignored in the current version. This keeps routing and persistence separate
    from the individual memory-processing components.
    """

    def __init__(self, db: Session) -> None:
        """Initialize the database session and memory pipeline components."""
        self.db = db
        self.extractor = MemoryExtractor()
        self.classifier = MemoryClassifier()
        self.importance_scorer = MemoryImportance()

    def process(self, memory: Memory) -> Memory | None:
        """Return an enriched memory after routing it to specialized storage.

        The method rejects non-memory-worthy content, classifies accepted
        content, assigns an importance score, and persists non-general
        memories. General memories are returned without being stored.
        """
        if not self.extractor.extract(memory.content):
            return None

        memory.category = self.classifier.classify(memory.content)
        memory.importance = self.importance_scorer.calculate(
            memory.content,
            memory.category,
        )
        self._persist_memory(memory)

        return memory

    def _persist_memory(self, memory: Memory) -> None:
        """Persist a memory in the specialized table for its category."""
        database_record = None

        if memory.category == "decision":
            database_record = Decision(
                content=memory.content,
                importance=memory.importance,
                project_id=memory.project_id,
            )
        elif memory.category == "knowledge":
            database_record = Knowledge(
                title=self._title_from_content(memory.content, 200),
                content=memory.content,
                category=memory.category,
                importance=memory.importance,
                project_id=memory.project_id,
            )
        elif memory.category == "research":
            database_record = Research(
                title=self._title_from_content(memory.content, 200),
                content=memory.content,
                source=memory.source,
                project_id=memory.project_id,
            )
        elif memory.category == "task":
            database_record = Task(
                title=self._title_from_content(memory.content, 150),
                description=memory.content,
                project_id=memory.project_id,
            )
        elif memory.category == "timeline":
            database_record = Timeline(
                event=self._title_from_content(memory.content, 200),
                description=memory.content,
                project_id=memory.project_id,
            )

        if database_record is None:
            return

        self.db.add(database_record)
        self.db.commit()
        self.db.refresh(database_record)

    @staticmethod
    def _title_from_content(content: str, max_length: int) -> str:
        """Create a table-compatible title or event from memory content."""
        return content[:max_length]
