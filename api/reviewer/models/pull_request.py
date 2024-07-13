"""Models for a pull request."""

from datetime import datetime

from pydantic import BaseModel


class PullRequest(BaseModel):
    """A pull request.

    Attributes
    ----------
    - id: The pull request ID.
    - user_id: The ID of the user who created the PR.
    - title: The PR title.
    - description: The PR description.
    - created_at: The creation date of the PR.
    - updated_at: The last update date of the PR.
    """

    id: int
    user_id: int
    title: str
    description: str
    created_at: datetime
    updated_at: datetime
