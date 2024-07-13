"""ORM for users."""

from typing import ClassVar

from sqlalchemy import Boolean, Column, Integer, String

from api.common.orm.base import Base
from api.config import config


class Users(Base):
    """ORM class to represent a user."""

    __tablename__ = "users"
    __table_args__: ClassVar = {"schema": config.database.common.app}

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    username = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)
    is_superuser = Column(Boolean, nullable=False)
