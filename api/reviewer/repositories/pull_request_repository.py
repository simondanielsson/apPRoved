from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload

from api.reviewer.dto.responses import ReviewResponse
from api.reviewer.models.pull_request import PullRequest
from api.reviewer.models.repository import Repository
from api.reviewer.models.review import Review
from api.reviewer.orm.pull_requests import PullRequests
from api.reviewer.orm.repositories import Repositories
from api.reviewer.orm.reviews import FileReviews, Reviews
from api.utils.database import database_session, orm_to_pydantic


async def list_repositories() -> list[Repository]:
    """List repositories."""
    async with database_session() as session:
        result = await session.execute(select(Repositories))
        repositories = result.scalars().all()
        return [orm_to_pydantic(repository, Repository) for repository in repositories]


async def add_repository(
    repository_name: str,
    github_url: str | None = None,
) -> Repository:
    """Add a repository."""
    async with database_session() as session:
        new_repository = Repositories(
            repository_name=repository_name,
            github_url=github_url,
        )
        session.add(new_repository)
        await session.commit()
        await session.refresh(new_repository)
        return orm_to_pydantic(new_repository, Repository)


async def delete_repository(repository_id: int) -> None:
    """Delete a repository."""
    async with database_session() as session:
        await session.execute(
            delete(Repositories).where(Repositories.id == repository_id),
        )
        await session.commit()


async def get_repository(repository_id: int) -> Repository:
    """Get a repository."""
    async with database_session() as session:
        result = await session.execute(
            select(Repositories).where(Repositories.id == repository_id),
        )
        repository = result.scalar()
        return orm_to_pydantic(repository, Repository)


async def add_pull_request(
    repository_id: int,
    pull_request_number: int,
) -> PullRequest:
    """Add a pull request."""
    async with database_session() as session:
        new_pull_request = PullRequests(
            repository_id=repository_id,
            pull_request_number=pull_request_number,
        )
        session.add(new_pull_request)
        await session.commit()
        await session.refresh(new_pull_request)
        return orm_to_pydantic(new_pull_request, PullRequest)


async def get_pull_requests(repository_id: int) -> list[PullRequest]:
    """Get a list of pull requests."""
    async with database_session() as session:
        result = await session.execute(
            select(PullRequests).where(PullRequests.repository_id == repository_id),
        )
        pull_requests = result.scalars().all()
        return [
            orm_to_pydantic(pull_request, PullRequest) for pull_request in pull_requests
        ]


async def get_pull_request(
    repository_id: int,
    pull_request_id: int,
) -> PullRequest:
    """Get a pull request."""
    async with database_session() as session:
        result = await session.execute(
            select(PullRequests).where(PullRequests.id == pull_request_id),
        )
        pull_request = result.scalar()
        return orm_to_pydantic(pull_request, PullRequest)


async def add_review(pull_request_id: int) -> Review:
    """Add a review."""
    async with database_session() as session:
        new_review = Reviews(
            pull_request_id=pull_request_id,
        )
        session.add(new_review)
        await session.commit()
        await session.refresh(new_review)
        return orm_to_pydantic(new_review, Review)


async def add_file_review(
    review_id: int,
    review_contents: list[str],
    file_names: list[str],
) -> None:
    """Add file reviews."""
    async with database_session() as session:
        file_reviews = []
        for review_content, file_name in zip(review_contents, file_names):
            file_review = FileReviews(
                review_id=review_id,
                content=review_content,
                file_name=file_name,
            )
            file_reviews.append(file_review)

        session.add_all(file_reviews)
        await session.commit()


async def get_reviews(
    repository_id: int,
    pull_request_id: int,
) -> list[Review]:
    """Get a list of reviews."""
    async with database_session() as session:
        result = await session.execute(
            select(Reviews).where(Reviews.pull_request_id == pull_request_id),
        )
        reviews = result.scalars().all()
        return [orm_to_pydantic(review, Review) for review in reviews]


async def get_review(
    repository_id: int,
    pull_request_id: int,
    review_id: int,
) -> ReviewResponse:
    """Get a review."""
    async with database_session() as session:
        result = await session.execute(
            select(Reviews)
            .options(
                selectinload(Reviews.file_reviews),
            )
            .where(Reviews.id == review_id),
        )
        review = result.scalars().first()
        if review is None:
            message = f"Review with id {review_id} not found."
            raise ValueError(message)
        review_contents = [file_review.content for file_review in review.file_reviews]
        file_names = [file_review.file_name for file_review in review.file_reviews]
        return ReviewResponse(
            review_id=review.id,
            review_contents=review_contents,
            file_names=file_names,
        )


async def delete_review(
    repository_id: int,
    pull_request_id: int,
    review_id: int,
) -> None:
    """Delete a review."""
    async with database_session() as session:
        await session.execute(
            delete(FileReviews).where(FileReviews.review_id == review_id),
        )
        await session.execute(
            delete(Reviews).where(Reviews.id == review_id),
        )

        await session.commit()
