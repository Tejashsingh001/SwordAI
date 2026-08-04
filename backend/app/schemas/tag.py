"""Pydantic schemas for reusable conversation tags."""

from pydantic import BaseModel, Field, field_validator


class TagCreate(BaseModel):
    """Data required to create or rename a tag."""

    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Tag name (2 to 50 characters).",
    )

    @field_validator("name", mode="before")
    @classmethod
    def strip_name_whitespace(cls, value: str) -> str:
        """Trim tag whitespace before length validation."""
        if isinstance(value, str):
            return value.strip()
        return value


class TagResponse(TagCreate):
    """Tag data returned by the API."""

    id: int

    class Config:
        from_attributes = True
