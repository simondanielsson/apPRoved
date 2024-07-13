"""User repository."""

from bcrypt import gensalt, hashpw
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql import select

from api.common.models.user import User
from api.common.orm.users import Users
from api.utils.database import database_session, orm_to_pydantic


async def read_user(username: str) -> User:
    """Read user.

    :param username: username of user to read.
    :return: user.
    """
    async with database_session() as session:
        existing_user = await _get_user_if_exists(
            username=username,
            session=session,
        )

        return orm_to_pydantic(existing_user, User)


async def _get_user_if_exists(
    username: str,
    session: AsyncSession,
) -> Users:
    """Get a user if it exists."""
    result = await session.execute(select(Users).where(Users.username == username))
    user = result.scalars().first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User not found for username: {username}",
        )

    return user


async def create_user(
    username: str,
    password: str,
) -> User:
    """Create a user."""
    async with database_session() as session:
        user = Users(
            username=username,
            password_hash=_get_password_hash(password),
            is_active=True,
            is_superuser=False,
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


def _get_password_hash(password: str) -> str:
    """Get a password hash."""
    return hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")
