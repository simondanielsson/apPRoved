"""ORM for pull requests."""

from typing import ClassVar

from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.orm.properties import ForeignKey

from api.common.orm.base import Base
from api.config import config


class PullRequests(Base):
    """ORM for pull requests."""

    __tablename__: str = "pullrequests"
    __table_args__: ClassVar = {"schema": config.database.reviewer.app}

    id = Column(Integer, primary_key=True, autoincrement=True)
    repository_id = Column(
        Integer,
        ForeignKey(f"{config.database.reviewer.app}.repositories.id"),
    )
    pull_request_number = Column(Integer, nullable=False)

    reviews = relationship("Reviews", back_populates="pull_request")
    repository = relationship("Repositories", back_populates="pull_requests")
