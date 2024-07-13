"""File to store global constants.

Do not put constants related to a single part of the app here.
"""

from enum import StrEnum


# FastAPI tags.
class ApplicationTags(StrEnum):
    """Tags for FastAPI."""

    DEFAULT_TAG = "default"
    REVIEWER_TAG = "reviewer"
