"""Pydantic request and response models for the SwordAI AI pipeline."""

from pydantic import BaseModel, Field


class AIRequest(BaseModel):
    """Input required to generate an AI response for a project."""

    project_id: int = Field(
        ...,
        gt=0,
        description="ID of the project that provides context for the request.",
    )
    user_query: str = Field(
        ...,
        min_length=1,
        description="The user's question or instruction for the AI assistant.",
    )


class AIResponse(BaseModel):
    """Generated AI text associated with the project used as context."""

    project_id: int = Field(
        ...,
        description="ID of the project used to generate the response.",
    )
    response: str = Field(
        ...,
        description="Generated text returned by the AI model.",
    )
    conversation_id: int | None = Field(
        default=None,
        description="Conversation associated with this AI interaction.",
    )
