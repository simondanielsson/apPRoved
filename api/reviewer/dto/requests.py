"""Request DTOs for reviewer module."""

from pydantic import BaseModel, Field


class RegisterPRRequest(BaseModel):
    """Request DTO for registering a PR."""

    pull_request_number: int


class AddRepositoryRequest(BaseModel):
    """Request DTO for adding a repository."""

    repository_name: str
    github_url: str = Field(default="https://github.com")
