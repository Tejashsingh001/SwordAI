from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class KnowledgeCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="Knowledge title (3 to 200 characters).",
    )
    content: str = Field(
        ...,
        min_length=5,
        max_length=10000,
        description="Knowledge content (5 to 10000 characters).",
    )
    category: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Knowledge category (2 to 100 characters).",
    )
    importance: int = Field(
        default=1,
        ge=1,
        description="Knowledge importance. Must be at least 1.",
    )
    project_id: int = Field(
        ...,
        gt=0,
        description="ID of the associated project. Must be greater than 0.",
    )

    @field_validator("title", "content", "category", mode="before")
    @classmethod
    def strip_whitespace(cls, value: str) -> str:
        if isinstance(value, str):
            return value.strip()
        return value


class KnowledgeResponse(KnowledgeCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
