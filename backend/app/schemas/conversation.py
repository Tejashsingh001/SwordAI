"""Pydantic schemas for Conversation API requests and responses."""

from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from app.schemas.tag import TagResponse


class ConversationCreate(BaseModel):
    """Data required to create or update a project conversation."""

    project_id: int = Field(
        ...,
        gt=0,
        description="ID of the project that owns this conversation.",
    )
    title: str | None = Field(
        default=None,
        max_length=200,
        description="Optional conversation title (up to 200 characters).",
    )
    summary: str | None = Field(
        default=None,
        max_length=500,
        description="Optional manually assigned conversation summary.",
    )
    is_pinned: bool | None = Field(
        default=None,
        description="Optional pinned state. Defaults to false when created.",
    )
    is_archived: bool | None = Field(
        default=None,
        description="Optional archive state. Defaults to false when created.",
    )

    @field_validator("title", "summary", mode="before")
    @classmethod
    def strip_optional_text_whitespace(cls, value: str | None) -> str | None:
        """Trim optional text fields before length validation."""
        if isinstance(value, str):
            return value.strip() or None
        return value


class ConversationResponse(ConversationCreate):
    """Conversation data returned by the API."""

    id: int
    title: str
    summary: str
    is_pinned: bool
    is_archived: bool
    tags: list[TagResponse] = Field(default_factory=list)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
