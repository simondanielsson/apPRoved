"""Authentication service."""

from typing import Annotated

from bcrypt import checkpw
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, OAuth2PasswordBearer
from jose import JWTError, jwt

import api.common.repositories.users as users_repository
from api.common.models.user import User
from api.config import config

security = HTTPBasic()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """Get the current user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            config.secret_key,
            algorithms=[config.secret_algorithm],
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception from e

    try:
        user = await users_repository.read_user(username=username)
        if user is None:
            raise credentials_exception
    except HTTPException as e:
        raise credentials_exception from e

    return user


async def authenticate_user(
    username: str,
    password: str,
) -> User:
    """Authenticate a user.

    :param credentials: The credentials to authenticate.
    :return: The authenticated user.
    """
    try:
        user = await users_repository.read_user(username=username)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username does not exist.",
            headers={"WWW-Authenticate": "Basic"},
        ) from None

    if not checkpw(
        password.encode("utf-8"),
        user.password_hash.encode("utf-8"),
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password.",
            headers={"WWW-Authenticate": "Basic"},
        )

    return user


async def create_user(
    username: str,
    password: str,
) -> User:
    """Create a user."""
    return await users_repository.create_user(
        username=username,
        password=password,
    )


def create_access_token(data: dict) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    to_encode.update({"sub": data["username"]})
    return jwt.encode(to_encode, config.secret_key, algorithm=config.secret_algorithm)
