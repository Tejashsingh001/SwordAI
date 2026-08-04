"""HTTP endpoints that expose the SwordAI AI workflow."""

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.orm import Session

from app.database.dependencies import get_db
from app.services.ai_service import AIService

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


class ChatRequest(BaseModel):
    """Project-scoped user input for the AI chat endpoint."""

    project_id: int = Field(
        ...,
        gt=0,
        description="ID of the project that provides the AI context.",
    )
    message: str = Field(
        ...,
        min_length=1,
        description="User message to process with the AI engine.",
    )
    conversation_id: int | None = Field(
        default=None,
        gt=0,
        description="Optional existing conversation ID for this interaction.",
    )

    @field_validator("message", mode="before")
    @classmethod
    def strip_message_whitespace(cls, value: str) -> str:
        """Trim message whitespace before validating its length."""
        if isinstance(value, str):
            return value.strip()
        return value


class ChatResponse(BaseModel):
    """Generated text returned by the AI chat endpoint."""

    response: str = Field(
        ...,
        description="Generated AI response text.",
    )
    conversation_id: int = Field(
        ...,
        description="Conversation that contains this interaction.",
    )


@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
) -> ChatResponse:
    """Delegate a project-scoped message to the AI Service."""
    service = AIService(db)
    ai_response = service.chat(
        request.project_id,
        request.message,
        request.conversation_id,
    )

    return ChatResponse(
        response=ai_response.response,
        conversation_id=ai_response.conversation_id,
    )
