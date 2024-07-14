"""ORM for reviews."""

from typing import ClassVar

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm.properties import ForeignKey

from api.common.orm.base import Base
from api.config import config


class Reviews(Base):
    """ORM for reviews."""

    __tablename__: str = "reviews"
    __table_args__: ClassVar = {"schema": config.database.reviewer.app}

    id = Column(Integer, primary_key=True, autoincrement=True)
    pull_request_id = Column(
        Integer,
        ForeignKey(f"{config.database.reviewer.app}.pullrequests.id"),
    )
    pull_request = relationship("PullRequests", back_populates="reviews")
    file_reviews = relationship("FileReviews", back_populates="review")


class FileReviews(Base):
    """Reviews for files."""

    __tablename__: str = "filereviews"
    __table_args__: ClassVar = {"schema": config.database.reviewer.app}

    id = Column(Integer, primary_key=True, autoincrement=True)
    review_id = Column(
        Integer,
        ForeignKey(f"{config.database.reviewer.app}.reviews.id"),
    )
    content = Column(String, nullable=False)
    file_name = Column(String, nullable=False)

    review = relationship("Reviews", back_populates="file_reviews")
