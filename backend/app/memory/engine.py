"""Public interface for SwordAI's Context and Memory Engine."""

from sqlalchemy.orm import Session

from app.memory.memory import Memory
from app.memory.storage import MemoryStorage


class ContextMemoryEngine:
    """Provide the public entry point for Context and Memory processing.

    Other backend modules should interact only with this class. The extractor,
    classifier, importance scorer, and storage coordinator remain internal
    implementation details behind this interface. Context retrieval and AI
    model calls are intentionally not part of this stage.
    """

    def __init__(self, db: Session) -> None:
        """Initialize the internal pipeline with a database session.

        The caller owns the injected session and its lifecycle.
        """
        self.storage = MemoryStorage(db)

    def process_memory(
        self,
        content: str,
        source: str,
        project_id: int | None = None,
        metadata: dict | None = None,
    ) -> Memory | None:
        """Process content and return it when it is suitable for memory.

        A Memory object is created from the public inputs and passed to the
        internal storage pipeline. Metadata defaults to an empty dictionary
        when no structured context is provided.
        """
        if metadata is None:
            metadata = {}

        memory = Memory(
            content=content,
            source=source,
            project_id=project_id,
            metadata=metadata,
        )
        return self.storage.process(memory)
