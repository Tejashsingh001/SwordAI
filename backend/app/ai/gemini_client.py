"""Gemini-specific client isolated from SwordAI's AI orchestration layer."""

import logging
import os
from typing import Any

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class GeminiClientError(RuntimeError):
    """Raised when Gemini cannot be configured or return generated text."""


class GeminiClient:
    """Send prompts to Gemini and return generated text.

    This class owns all Gemini SDK interaction. It loads the API key from the
    environment after reading the project's .env file and exposes no provider
    details to the rest of the AI pipeline.
    """

    def __init__(
        self,
        model_name: str | None = None,
        client: Any | None = None,
    ) -> None:
        """Initialize the Gemini client using the configured API key."""
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            logger.error("GEMINI_API_KEY is not configured.")
            raise GeminiClientError("GEMINI_API_KEY is not configured.")

        self.model_name = model_name or os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash",
        )
        self.client = client or self._create_client(api_key)

    def generate(self, prompt: str) -> str:
        """Send a prompt to Gemini and return only its generated text.

        Connection and provider errors are logged and exposed as a stable
        application exception without leaking the API key or prompt content.
        """
        logger.info(
            "Sending a prompt to Gemini using model=%s.",
            self.model_name,
        )

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
            )
        except Exception as error:
            logger.exception("Gemini generation failed.")
            raise GeminiClientError(
                "Unable to generate an AI response."
            ) from error

        response_text = getattr(response, "text", None)

        if not response_text:
            logger.error("Gemini returned an empty response.")
            raise GeminiClientError("Gemini returned no generated text.")

        logger.info("Received generated text from Gemini.")
        return response_text

    @staticmethod
    def _create_client(api_key: str) -> Any:
        """Create the official Gemini SDK client only when it is needed."""
        try:
            from google import genai
        except ImportError as error:
            logger.exception("The google-genai package is unavailable.")
            raise GeminiClientError(
                "Gemini support requires the google-genai package."
            ) from error

        return genai.Client(api_key=api_key)
