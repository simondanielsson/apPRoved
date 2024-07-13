"""Request DTOs for the API."""

from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    """Request DTO for creating a user."""

    username: str
    password: str
