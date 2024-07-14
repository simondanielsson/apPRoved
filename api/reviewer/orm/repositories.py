"""ORM for the repositories table."""

from typing import ClassVar

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from api.common.orm.base import Base
from api.config import config


class Repositories(Base):
    """A github repository."""

    __tablename__: str = "repositories"
    __table_args__: ClassVar = {"schema": config.database.reviewer.app}

    id = Column(Integer, primary_key=True, autoincrement=True)
    github_url = Column(
        String,
        nullable=False,
        default="api.github.com",
    )  # github.yourcompany.com/api/v3 for enterprise
    repository_name = Column(String, nullable=False)

    pull_requests = relationship("PullRequests", back_populates="repository")
