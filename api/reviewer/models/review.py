"""Models for a PR review."""

from pydantic import BaseModel


class Review(BaseModel):
    """A PR review.

    Attributes
    ----------
    - id: The review ID.
    - pull_request_id: The Pull Request ID.
    - content: The review content.
    """

    id: int
    pull_request_id: int
    content: str

    class Config:
        """Config class."""

        from_attributes = True
