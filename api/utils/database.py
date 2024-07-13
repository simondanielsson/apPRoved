"""Database utilities."""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator, TypeVar

import sqlalchemy
from box import Box
from pydantic import BaseModel
from sqlalchemy import engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from api.common.orm.base import Base
from api.config import config

logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


def create_connection_url(database_config: Box) -> engine.url.URL:
    """Create a connection URL from a database configuration.

    :param database_config: the database configuration.
    :return: the connection URL.
    """
    return engine.url.URL.create(
        drivername=database_config.dialect,
        username=database_config.username,
        password=database_config.password,
        host=database_config.host,
        port=database_config.port,
        database=database_config.db_name,
    )


async_engine: AsyncEngine = create_async_engine(
    url=create_connection_url(config.database),
    echo=True,
)
async_session = sessionmaker(
    async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


@asynccontextmanager
async def database_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a transactional scope around a series of operations."""
    async with async_session() as session:
        yield session


async def init_db() -> None:
    """Initialize the database."""
    async with async_engine.begin() as conn:
        for schema in (config.database.common.app, config.database.reviewer.app):
            await conn.execute(sqlalchemy.text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
        await conn.run_sync(Base.metadata.create_all)


TypeVarBaseModel = TypeVar("TypeVarBaseModel", bound=BaseModel)
TypeVarORMModel = TypeVar("TypeVarORMModel", bound=Base)


def orm_to_pydantic(
    orm_object: TypeVarORMModel,
    pydantic_class: type[TypeVarBaseModel],
) -> TypeVarBaseModel:
    """Convert an ORM object to a Pydantic object.

    :param orm_object: the ORM object to convert.
    :param pydantic_class: the Pydantic class of the resulting object.
    :return: the Pydantic object.
    """
    return pydantic_class.model_validate(orm_object, from_attributes=True)


def pydantic_to_orm(
    pydantic_object: BaseModel,
    orm_class: type[TypeVarORMModel],
) -> TypeVarORMModel:
    """Convert a Pydantic object to an ORM object.

    :param pydantic_object: the Pydantic object to convert.
    :param orm_class: the ORM class of the resulting object.
    :return: the ORM object.
    """
    return orm_class(**pydantic_object.model_dump())
