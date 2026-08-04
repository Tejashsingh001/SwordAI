"""Application service that connects AI HTTP requests to the AI Engine."""

import logging
from typing import Literal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.ai.ai_engine import AIEngine
from app.ai.models import AIResponse
from app.memory.engine import ContextMemoryEngine
from app.models.conversation import Conversation
from app.schemas.conversation import ConversationCreate
from app.schemas.message import MessageCreate
from app.services import conversation_service, message_service

logger = logging.getLogger(__name__)


class AIService:
    """Coordinate project chat persistence and the AI workflow engine.

    Conversation and message services manage persistence. AIEngine handles AI
    orchestration, while ContextMemoryEngine retains all memory-processing
    behavior after a complete interaction has been saved.
    """

    def __init__(self, db: Session) -> None:
        """Initialize the service with an injected SQLAlchemy session."""
        self.db = db

    def chat(
        self,
        project_id: int,
        message: str,
        conversation_id: int | None = None,
    ) -> AIResponse:
        """Save a complete interaction and return its AI response."""
        logger.info(
            "Delegating AI chat request for project_id=%s.",
            project_id,
        )
        conversation = self._get_or_create_conversation(
            project_id,
            message,
            conversation_id,
        )
        self._save_message(conversation.id, "user", message)

        engine = AIEngine(self.db)
        response = engine.process(project_id, message)
        self._save_message(conversation.id, "assistant", response.response)
        self._store_interaction_memories(
            project_id,
            message,
            response.response,
        )
        logger.info("Completed AI chat request for project_id=%s.", project_id)

        return AIResponse(
            project_id=project_id,
            response=response.response,
            conversation_id=conversation.id,
        )

    def _get_or_create_conversation(
        self,
        project_id: int,
        message: str,
        conversation_id: int | None,
    ) -> Conversation:
        """Load an owned conversation or create one from the first message."""
        if conversation_id is None:
            return conversation_service.create_conversation(
                ConversationCreate(project_id=project_id),
                self.db,
                first_message=message,
            )

        conversation = conversation_service.get_conversation(
            conversation_id,
            self.db,
        )

        if conversation.project_id != project_id:
            logger.warning(
                "Conversation project mismatch: conversation_id=%s.",
                conversation_id,
            )
            raise HTTPException(
                status_code=404,
                detail="Conversation not found for this project",
            )

        return conversation

    def _save_message(
        self,
        conversation_id: int,
        role: Literal["user", "assistant"],
        content: str,
    ) -> None:
        """Persist a user or assistant message through the Message Service."""
        message_service.create_message(
            MessageCreate(
                conversation_id=conversation_id,
                role=role,
                content=content,
            ),
            self.db,
        )

    def _store_interaction_memories(
        self,
        project_id: int,
        user_message: str,
        assistant_message: str,
    ) -> None:
        """Submit saved interaction text to the Context and Memory Engine.

        Memory persistence is best-effort so a memory failure cannot discard an
        otherwise successful response or its stored conversation messages.
        """
        memory_engine = ContextMemoryEngine(self.db)

        for source, content in (
            ("user_message", user_message),
            ("ai_response", assistant_message),
        ):
            try:
                memory_engine.process_memory(
                    content=content,
                    source=source,
                    project_id=project_id,
                )
                logger.info(
                    "Submitted %s to the memory engine for project_id=%s.",
                    source,
                    project_id,
                )
            except Exception:
                logger.exception(
                    "Memory processing failed for source=%s, project_id=%s.",
                    source,
                    project_id,
                )
