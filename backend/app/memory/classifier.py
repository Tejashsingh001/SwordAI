"""Rule-based classification of memory candidates into core categories."""


class MemoryClassifier:
    """Classify memory candidates for downstream storage and retrieval.

    This initial implementation uses explicit keyword matching because it is
    predictable and lightweight. Future versions will use LLM-based semantic
    classification to understand meaning beyond the words used in a message.
    """

    CATEGORY_KEYWORDS = (
        (
            "decision",
            ("decided", "decision", "choose", "selected", "architecture"),
        ),
        (
            "knowledge",
            ("know", "learned", "information", "concept", "explanation"),
        ),
        (
            "task",
            ("todo", "task", "implement", "build", "create", "finish"),
        ),
        ("research", ("research", "investigate", "compare", "study")),
        (
            "timeline",
            ("today", "tomorrow", "yesterday", "deadline", "milestone"),
        ),
    )

    def classify(self, text: str) -> str:
        """Return the first category whose keywords occur in text.

        Matching ignores case. Messages without a category signal are assigned
        to the general category.
        """
        normalized_text = text.casefold()

        for category, keywords in self.CATEGORY_KEYWORDS:
            if any(keyword in normalized_text for keyword in keywords):
                return category

        return "general"
