from typing import Literal

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=150,
        description="Task title (3 to 150 characters).",
    )
    description: str = Field(
        ...,
        min_length=5,
        max_length=1000,
        description="Task description (5 to 1000 characters).",
    )
    status: Literal["Pending", "In Progress", "Completed"] = Field(
        default="Pending",
        description="Task status. Must be Pending, In Progress, or Completed.",
    )
    project_id: int = Field(
        ...,
        gt=0,
        description="ID of the associated project. Must be greater than 0.",
    )


class TaskResponse(TaskCreate):
    id: int

    class Config:
        from_attributes = True
