from pydantic import BaseModel, Field, field_validator


class ResearchCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=200,
        description="Research title (3 to 200 characters).",
    )
    content: str = Field(
        ...,
        min_length=5,
        max_length=10000,
        description="Research content (5 to 10000 characters).",
    )
    source: str | None = Field(
        default=None,
        max_length=500,
        description="Optional source reference (up to 500 characters).",
    )
    project_id: int = Field(
        ...,
        gt=0,
        description="ID of the associated project. Must be greater than 0.",
    )

    @field_validator("title", "content", "source", mode="before")
    @classmethod
    def strip_whitespace(cls, value: str | None) -> str | None:
        if isinstance(value, str):
            return value.strip()
        return value


class ResearchResponse(ResearchCreate):
    id: int

    class Config:
        from_attributes = True
