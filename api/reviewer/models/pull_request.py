"""Models for a pull request."""


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
    repository_id: int
    pull_request_number: int


class PullRequestFileChanges(BaseModel):
    """Changes made to a file in a pull request."""

    filename: str
    patch: str
    additions: int
    deletions: int
    changes: int
