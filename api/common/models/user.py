"""User model."""

from pydantic import BaseModel


class User(BaseModel):
    """A user.

    Attributes
    ----------
    - id: The user ID.
    - username: The username.
    - is_active: Whether the user is active.
    - is_superuser: Whether the user is a superuser.
    """

    id: int
    username: str
    password_hash: str
    is_active: bool
    is_superuser: bool
