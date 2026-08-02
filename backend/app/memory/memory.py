"""Internal data object used throughout the Context and Memory Engine."""

from typing import Any

from pydantic import BaseModel, Field


class Memory(BaseModel):
    """Represents a unit of contextual information handled by the engine."""

    content: str = Field(
        ...,
        description="The textual information stored in this memory.",
    )
    source: str = Field(
        ...,
        description="The origin from which this memory was obtained.",
    )
    category: str | None = Field(
        default=None,
        description="An optional category used to classify this memory.",
    )
    importance: int = Field(
        default=0,
        description="The relative importance assigned to this memory.",
    )
    project_id: int | None = Field(
        default=None,
        description="The optional project identifier associated with this memory.",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional structured context associated with this memory.",
    )
