"""File to store global constants.

Do not put constants related to a single part of the app here.
"""

from enum import StrEnum


# FastAPI tags.
class ApplicationTags(StrEnum):
    """Tags for FastAPI."""

    DEFAULT_TAG = "default"
    REVIEWER_TAG = "reviewer"


class Tools(StrEnum):
    """Tools accomplish steps in a chain."""

    REVIEW_PULL_REQUEST = "review_pull_request"


class LLMProvider(StrEnum):
    """LLM providers."""

    OPENAI = "openai"
