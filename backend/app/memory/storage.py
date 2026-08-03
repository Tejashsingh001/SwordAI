"""Persistence pipeline for extracted, classified, and scored memories."""

from sqlalchemy.orm import Session

from app.memory.classifier import MemoryClassifier
from app.memory.extractor import MemoryExtractor
from app.memory.importance import MemoryImportance
from app.memory.memory import Memory
from app.memory.repository import MemoryRepository


class MemoryStorage:
    """Coordinate the memory pipeline and persist specialized records.

    The repository persists specialized records after extraction,
    classification, and importance scoring. General memories are intentionally
    ignored in the current version. This keeps pipeline orchestration separate
    from individual processing components and database access.
    """

    def __init__(self, db: Session) -> None:
        """Initialize the database session and memory pipeline components."""
        self.db = db
        self.extractor = MemoryExtractor()
        self.classifier = MemoryClassifier()
        self.importance_scorer = MemoryImportance()
        self.repository = MemoryRepository(db)

    def process(self, memory: Memory) -> Memory | None:
        """Return an enriched memory after it is saved through the repository.

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
        self.repository.save_memory(memory)

        return memory
