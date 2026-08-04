"""Persistence pipeline for extracted, classified, and scored memories."""

from sqlalchemy.orm import Session

from app.memory.classifier import MemoryClassifier
from app.memory.extractor import MemoryExtractor
from app.memory.importance import MemoryImportance
from app.memory.memory import Memory
from app.memory.repository import MemoryRepository


class MemoryStorage:
    """Coordinate the memory pipeline and persist accepted memories.

    The repository persists memories after extraction, classification,
    and importance scoring. MemoryStorage is responsible for orchestrating
    the processing pipeline while keeping extraction, classification,
    importance scoring, and database access separated into dedicated
    components.
    """

    def __init__(self, db: Session) -> None:
        """Initialize the database session and memory pipeline components."""
        self.db = db
        self.extractor = MemoryExtractor()
        self.classifier = MemoryClassifier()
        self.importance_scorer = MemoryImportance()
        self.repository = MemoryRepository(db)

    def process(self, memory: Memory) -> Memory | None:
        """Process, enrich, and persist a memory.

        The method performs the following steps:

        1. Determine whether the content is memory-worthy.
        2. Classify the memory.
        3. Calculate its importance score.
        4. Persist the enriched memory through the repository.

        Returns:
            The enriched Memory object if the content is accepted,
            otherwise None.
        """
        # Reject content that should not become memory.
        if not self.extractor.extract(memory.content):
            return None

        # Categorize the memory.
        memory.category = self.classifier.classify(memory.content)

        # Score the memory's importance.
        memory.importance = self.importance_scorer.calculate(
            memory.content,
            memory.category,
        )

        # Persist the processed memory.
        self.repository.save_memory(memory)

        return memory