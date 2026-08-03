"""Rule-based retrieval of relevant project context from stored memories."""

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import TypeAlias

from app.memory.repository import MemoryRepository, StoredMemory

RankedMemory: TypeAlias = tuple[int, int, bool, bool, float, StoredMemory]


@dataclass
class Context:
    """The selected memories and metadata needed to augment a user query."""

    relevant_memories: list[StoredMemory]
    project_id: int
    retrieved_at: datetime


class ContextRetriever:
    """Select the most relevant stored memories for an incoming query.

    Retrieval remains rule-based in this version: it uses keyword overlap and
    metadata available from the specialized SQLAlchemy models. Embeddings,
    vector databases, and AI-powered ranking are intentionally deferred.
    """

    def __init__(self, repository: MemoryRepository) -> None:
        """Initialize the retriever with an injected memory repository."""
        self.repository = repository

    def retrieve(
        self,
        query: str,
        project_id: int,
        limit: int = 10,
    ) -> Context:
        """Return up to limit project memories that match the query.

        Keyword overlap determines relevance. Importance and recency rank
        matching memories with the same overlap score, and duplicate content
        is removed before the result is returned.
        """
        if limit <= 0:
            return Context(
                relevant_memories=[],
                project_id=project_id,
                retrieved_at=datetime.now(timezone.utc),
            )

        query_keywords = self._keywords(query)
        project_memories = self.repository.get_project_memories(project_id)
        important_memories = self.repository.get_important_memories(project_id)
        recent_memories = self.repository.get_recent_memories(
            project_id,
            limit=max(limit, 20),
        )

        important_ids = {
            self._record_identity(memory)
            for memory in important_memories
        }
        recent_ids = {
            self._record_identity(memory)
            for memory in recent_memories
        }
        ranked_memories: list[RankedMemory] = []

        for memory in project_memories:
            memory_keywords = self._keywords(self._content(memory))
            overlap_score = len(query_keywords & memory_keywords)

            if overlap_score == 0:
                continue

            ranked_memories.append(
                (
                    overlap_score,
                    self._importance(memory),
                    self._record_identity(memory) in important_ids,
                    self._record_identity(memory) in recent_ids,
                    self._created_timestamp(memory),
                    memory,
                )
            )

        ranked_memories.sort(
            key=lambda item: item[:5],
            reverse=True,
        )

        relevant_memories = self._remove_duplicates(ranked_memories, limit)
        return Context(
            relevant_memories=relevant_memories,
            project_id=project_id,
            retrieved_at=datetime.now(timezone.utc),
        )

    @staticmethod
    def _keywords(text: str) -> set[str]:
        """Extract normalized words used for rule-based overlap matching."""
        return set(re.findall(r"\b\w+\b", text.casefold()))

    @staticmethod
    def _content(memory: StoredMemory) -> str:
        """Return the text field that best represents a specialized record."""
        return (
            getattr(memory, "content", None)
            or getattr(memory, "description", None)
            or getattr(memory, "title", None)
            or getattr(memory, "event", "")
        )

    @staticmethod
    def _importance(memory: StoredMemory) -> int:
        """Return a record's stored importance or a neutral default."""
        return getattr(memory, "importance", 0) or 0

    @staticmethod
    def _record_identity(memory: StoredMemory) -> tuple[str, int | None]:
        """Build an identity that remains unique across specialized tables."""
        return type(memory).__name__, getattr(memory, "id", None)

    @staticmethod
    def _created_timestamp(memory: StoredMemory) -> float:
        """Return a comparable timestamp for records with date metadata."""
        created_at = getattr(memory, "created_at", None)

        if not isinstance(created_at, datetime):
            return 0.0

        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)

        return created_at.timestamp()

    def _remove_duplicates(
        self,
        ranked_memories: list[RankedMemory],
        limit: int,
    ) -> list[StoredMemory]:
        """Return the highest-ranked record for each unique memory content."""
        seen_content: set[str] = set()
        relevant_memories: list[StoredMemory] = []

        for _, _, _, _, _, memory in ranked_memories:
            normalized_content = " ".join(
                self._content(memory).casefold().split()
            )

            if normalized_content in seen_content:
                continue

            seen_content.add(normalized_content)
            relevant_memories.append(memory)

            if len(relevant_memories) == limit:
                break

        return relevant_memories
