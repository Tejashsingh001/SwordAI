"""Provider-agnostic orchestration for SwordAI's AI workflow."""

import logging

from sqlalchemy.orm import Session

from app.ai.gemini_client import GeminiClient, GeminiClientError
from app.ai.models import AIResponse
from app.ai.prompt_builder import PromptBuilder
from app.memory.repository import MemoryRepository
from app.memory.retriever import ContextRetriever
from app.models.project import Project

logger = logging.getLogger(__name__)


class AIEngineError(RuntimeError):
    """Raised when the AI workflow cannot create a response."""


class AIEngine:
    """Coordinate retrieval, prompt generation, and AI response delivery.

    The engine is the provider-agnostic AI workflow boundary. Gemini-specific
    communication stays inside GeminiClient, keeping the engine ready for a
    future provider replacement without altering retrieval or prompt logic.
    """

    def __init__(
        self,
        db: Session,
        gemini_client: GeminiClient | None = None,
    ) -> None:
        """Initialize AI workflow dependencies with an injected session."""
        self.db = db
        self.repository = MemoryRepository(db)
        self.retriever = ContextRetriever(self.repository)
        self.prompt_builder = PromptBuilder()
        self.gemini_client = gemini_client or GeminiClient()

    def process(self, project_id: int, user_query: str) -> AIResponse:
        """Generate an AI response for a project-scoped user request."""
        logger.info("Processing AI request for project_id=%s.", project_id)

        try:
            project = self._get_project(project_id)
            context = self.retriever.retrieve(user_query, project_id)
            prompt = self.prompt_builder.build_prompt(
                user_query,
                context,
                project,
            )
            response_text = self.gemini_client.generate(prompt.final_prompt)
        except GeminiClientError as error:
            logger.error(
                "Gemini request failed for project_id=%s.",
                project_id,
            )
            raise AIEngineError(
                "Unable to generate an AI response."
            ) from error
        except AIEngineError:
            raise
        except Exception as error:
            logger.exception(
                "AI workflow failed for project_id=%s.",
                project_id,
            )
            raise AIEngineError("Unable to process the AI request.") from error

        logger.info("Completed AI request for project_id=%s.", project_id)
        return AIResponse(project_id=project_id, response=response_text)

    def _get_project(self, project_id: int) -> Project:
        """Return the requested project or raise a workflow-level error."""
        project = self.db.query(Project).filter(
            Project.id == project_id
        ).first()

        if project is None:
            logger.warning(
                "Project not found for AI request: project_id=%s.",
                project_id,
            )
            raise AIEngineError("Project not found.")

        return project
