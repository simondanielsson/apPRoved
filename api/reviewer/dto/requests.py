"""Request DTOs for reviewer module."""

from pydantic import BaseModel, Field


class RegisterPRRequest(BaseModel):
    """Request DTO for registering a PR.

    Attributes
    ----------
    - pull_request_url: The URL of the pull request.
    """

    pull_request_url: str


class CreateReviewRequest(BaseModel):
    """Request for creating a PR review using AI."""

    repository: str
    pull_request_number: int


class AddRepositoryRequest(BaseModel):
    """Request DTO for adding a repository."""

    repository_owner: str
    repository: str
    github_url: str = Field(default="https://github.com")
