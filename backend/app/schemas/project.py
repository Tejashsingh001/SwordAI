from pydantic import BaseModel, Field, field_validator


class ProjectCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Project name (3 to 100 characters).",
    )
    description: str = Field(
        ...,
        min_length=5,
        max_length=1000,
        description="Project description (5 to 1000 characters).",
    )

    @field_validator("name", "description", mode="before")
    @classmethod
    def strip_whitespace(cls, value: str) -> str:
        if isinstance(value, str):
            return value.strip()
        return value


class ProjectResponse(ProjectCreate):
    id: int

    class Config:
        from_attributes = True
