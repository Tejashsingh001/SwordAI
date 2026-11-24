"""Unit tests for SwordAI's deterministic memory-rule components."""

import pytest

from app.memory.classifier import MemoryClassifier
from app.memory.extractor import MemoryExtractor
from app.memory.importance import MemoryImportance


@pytest.mark.parametrize(
    "text",
    [
        "We DECIDED to remember this.",
        "The architecture is important.",
        "Never lose project knowledge.",
    ],
)
def test_extractor_accepts_case_insensitive_memory_keywords(text: str) -> None:
    """Extractor accepts text containing any configured keyword."""
    assert MemoryExtractor().extract(text) is True


def test_extractor_rejects_text_without_memory_keywords() -> None:
    """Extractor rejects text that does not contain a configured substring."""
    assert MemoryExtractor().extract("A short greeting without signals.") is False


@pytest.mark.parametrize(
    ("text", "category"),
    [
        ("We SELECTED a design.", "decision"),
        ("I LEARNED this concept.", "knowledge"),
        ("Please IMPLEMENT the API.", "task"),
        ("We should INVESTIGATE alternatives.", "research"),
        ("The deadline is tomorrow.", "timeline"),
        ("A neutral greeting.", "general"),
    ],
)
def test_classifier_returns_the_matching_category(
    text: str,
    category: str,
) -> None:
    """Classifier uses case-insensitive keyword matching by category order."""
    assert MemoryClassifier().classify(text) == category


def test_classifier_uses_first_matching_category_in_declared_order() -> None:
    """Decision wins when text contains both decision and task keywords."""
    assert MemoryClassifier().classify("Decided to implement it.") == "decision"


@pytest.mark.parametrize(
    ("category", "expected_score"),
    [
        ("decision", 9),
        ("knowledge", 8),
        ("research", 7),
        ("task", 6),
        ("timeline", 5),
        ("general", 3),
        ("unknown", 3),
    ],
)
def test_importance_uses_base_scores_and_general_fallback(
    category: str,
    expected_score: int,
) -> None:
    """Importance uses documented bases and defaults unknown categories."""
    assert MemoryImportance().calculate("neutral text", category) == expected_score


def test_importance_applies_case_insensitive_high_and_low_adjustments() -> None:
    """High and low signals each apply exactly one point of adjustment."""
    scorer = MemoryImportance()

    assert scorer.calculate("This is CRITICAL.", "task") == 7
    assert scorer.calculate("Perhaps this is later.", "task") == 5
    assert scorer.calculate("Important, but maybe temporary.", "task") == 6


def test_importance_caps_the_decision_score_at_ten() -> None:
    """The scorer limits high-priority decision text to the maximum score."""
    assert MemoryImportance().calculate("Always use this architecture.", "decision") == 10
