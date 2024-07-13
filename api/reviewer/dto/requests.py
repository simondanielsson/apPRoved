"""Request DTOs for reviewer module."""

from pydantic import BaseModel


class RegisterPRRequest(BaseModel):
    """Requqest DTO for registering a PR.

    Attributes
    ----------
    - pull_request_url: The URL of the pull request.
    """

    pull_request_url: str
