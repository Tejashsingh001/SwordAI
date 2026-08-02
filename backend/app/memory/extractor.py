"""Rule-based extraction of messages that may be worth remembering."""


class MemoryExtractor:
    """Identify messages that are likely valuable to the memory system.

    This first implementation uses a deterministic keyword check because it is
    lightweight, predictable, and requires no external model. It will later be
    replaced or enhanced with an AI-based extractor that can evaluate context
    and meaning beyond explicit keywords.
    """

    MEMORY_KEYWORDS = (
        "decided",
        "decision",
        "use",
        "architecture",
        "remember",
        "important",
        "always",
        "never",
        "project",
        "knowledge",
    )

    def extract(self, text: str) -> bool:
        """Return whether text contains a keyword that signals useful memory.

        Matching is case-insensitive so that keyword capitalization does not
        affect whether the message is selected for memory processing.
        """
        normalized_text = text.casefold()
        return any(keyword in normalized_text for keyword in self.MEMORY_KEYWORDS)
