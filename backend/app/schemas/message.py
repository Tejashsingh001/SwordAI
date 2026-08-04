"""Pydantic schemas for Message API requests and responses."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class MessageCreate(BaseModel):
    """Data required to create or update a conversation message."""

    conversation_id: int = Field(
        ...,
        gt=0,
        description="ID of the conversation that owns this message.",
    )
    role: Literal["user", "assistant"] = Field(
        ...,
        description="Message author role. Must be user or assistant.",
    )
    content: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="Message content (1 to 10000 characters).",
    )

    @field_validator("content", mode="before")
    @classmethod
    def strip_content_whitespace(cls, value: str) -> str:
        """Trim message content before validating its length."""
        if isinstance(value, str):
            return value.strip()
        return value


class MessageResponse(MessageCreate):
    """Message data returned by the API."""

    id: int
    created_at: datetime

    class Config:
        from_attributes = True
