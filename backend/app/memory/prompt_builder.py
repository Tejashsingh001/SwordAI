"""Prompt-building interface for composing context-aware model prompts."""


class MemoryPromptBuilder:
    """Defines the contract for building prompts from retrieved memories."""

    def build_prompt(self):
        """Build a context-aware prompt from relevant memories."""
        raise NotImplementedError()
