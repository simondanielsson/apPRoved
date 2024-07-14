"""Module for the repository model."""

from pydantic import BaseModel


class Repository(BaseModel):
    """A github repository."""

    id: int
    github_url: str
    repository_name: str
