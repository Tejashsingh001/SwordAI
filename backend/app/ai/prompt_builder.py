"""Construction of context-aware prompts for future AI model integrations."""

from dataclasses import dataclass

from app.memory.repository import StoredMemory
from app.memory.retriever import Context
from app.models.project import Project


@dataclass(frozen=True)
class Prompt:
    """Structured prompt sections ready for a future AI model client.

    Attributes:
        system_prompt: Defines the assistant's project-centric role.
        project_context: Contains the current project's identifying details.
        memory_context: Contains relevant memories selected for the query.
        user_prompt: Contains the original user request.
        final_prompt: Combines every prompt section in the required order.
    """

    system_prompt: str
    project_context: str
    memory_context: str
    user_prompt: str
    final_prompt: str


class PromptBuilder:
    """Build prompts from a project, retrieved context, and user request.

    This class prepares text only. It is intentionally independent of Gemini,
    OpenAI, or any other model-provider API and does not send prompts itself.
    """

    def build_prompt(
        self,
        user_query: str,
        context: Context,
        project: Project,
    ) -> Prompt:
        """Build and return the complete prompt for a user request."""
        system_prompt = (
            "SYSTEM\n"
            "SwordAI is a project-centric AI assistant that uses project "
            "context to provide accurate, useful help."
        )
        project_context = (
            "PROJECT\n"
            f"Name: {project.name}\n"
            f"Description: {project.description}"
        )
        memory_context = self._build_memory_context(context.relevant_memories)
        user_prompt = f"USER REQUEST\n{user_query}"
        instructions = (
            "INSTRUCTIONS\n"
            "Answer using project memories whenever possible.\n"
            "If memories are insufficient, answer normally.\n"
            "Never invent project facts."
        )
        final_prompt = "\n\n".join(
            (
                system_prompt,
                project_context,
                memory_context,
                user_prompt,
                instructions,
            )
        )

        return Prompt(
            system_prompt=system_prompt,
            project_context=project_context,
            memory_context=memory_context,
            user_prompt=user_prompt,
            final_prompt=final_prompt,
        )

    def _build_memory_context(self, memories: list[StoredMemory]) -> str:
        """Format retrieved specialized records as a memory prompt section."""
        if not memories:
            return "MEMORIES\nNo relevant project memories were retrieved."

        formatted_memories = [
            self._format_memory(memory)
            for memory in memories
        ]
        return "MEMORIES\n" + "\n\n".join(formatted_memories)

    @staticmethod
    def _format_memory(memory: StoredMemory) -> str:
        """Format a specialized model record with category and importance."""
        category = (
            getattr(memory, "category", None)
            or type(memory).__name__.lower()
        )
        importance = getattr(memory, "importance", 0) or 0
        content = (
            getattr(memory, "content", None)
            or getattr(memory, "description", None)
            or getattr(memory, "title", None)
            or getattr(memory, "event", "")
        )

        return (
            f"- Category: {category}\n"
            f"  Importance: {importance}\n"
            f"  Memory: {content}"
        )
