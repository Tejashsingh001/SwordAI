"""Rule-based importance scoring for memory candidates."""


class MemoryImportance:
    """Assign a priority score before a memory is stored or retrieved.

    Importance helps the memory system prioritize durable, high-value context
    over less significant information. This initial rule-based approach is
    transparent and lightweight; future versions will use AI-based importance
    estimation to account for context and semantic meaning.
    """

    BASE_SCORES = {
        "decision": 9,
        "knowledge": 8,
        "research": 7,
        "task": 6,
        "timeline": 5,
        "general": 3,
    }
    HIGH_IMPORTANCE_KEYWORDS = (
        "always",
        "never",
        "architecture",
        "critical",
        "important",
        "permanent",
        "core",
    )
    LOW_IMPORTANCE_KEYWORDS = (
        "maybe",
        "perhaps",
        "probably",
        "temporary",
        "later",
    )

    def calculate(self, text: str, category: str) -> int:
        """Calculate an importance score from 1 to 10 for a memory candidate.

        A category determines the base score. High-importance and
        low-importance language adjust that base score by one point each.
        """
        normalized_text = text.casefold()
        score = self.BASE_SCORES.get(
            category.casefold(),
            self.BASE_SCORES["general"],
        )

        if any(
            keyword in normalized_text
            for keyword in self.HIGH_IMPORTANCE_KEYWORDS
        ):
            score += 1

        if any(
            keyword in normalized_text
            for keyword in self.LOW_IMPORTANCE_KEYWORDS
        ):
            score -= 1

        return max(1, min(score, 10))
