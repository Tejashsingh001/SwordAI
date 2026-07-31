from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class TimelineCreate(BaseModel):
    event: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="Timeline event (3 to 200 characters).",
    )
    description: str = Field(
        ...,
        min_length=5,
        max_length=1000,
        description="Event description (5 to 1000 characters).",
    )
    project_id: int = Field(
        ...,
        gt=0,
        description="ID of the associated project. Must be greater than 0.",
    )

    @field_validator("event", "description", mode="before")
    @classmethod
    def strip_whitespace(cls, value: str) -> str:
        if isinstance(value, str):
            return value.strip()
        return value


class TimelineResponse(TimelineCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
