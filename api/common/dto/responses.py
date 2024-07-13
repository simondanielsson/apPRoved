"""Response DTOs for the API."""

from pydantic import BaseModel


class TokenResponse(BaseModel):
    """Response DTO for a JWT access token."""

    access_token: str
    token_type: str


class UserResponse(BaseModel):
    """Response DTO for a user."""

    id: int
    username: str
    is_active: bool
    is_superuser: bool
