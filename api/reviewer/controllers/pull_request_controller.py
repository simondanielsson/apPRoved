"""Controller for pull request related operations."""

from api.reviewer.dto.responses import ReviewResponse
from api.reviewer.models.pull_request import PullRequest
from api.reviewer.models.repository import Repository
from api.reviewer.models.review import Review
from api.reviewer.services import pull_request_service


async def create_review(
    repository_id: int,
    pull_request_id: int,
) -> ReviewResponse:
    """Create a review.

    :param repository: The repository name ($OWNER/$REPOSITORY_NAME).
    :param pull_request_number: The pull request number.
    :return: The review ID.
    """
    return await pull_request_service.create_review(
        repository_id=repository_id,
        pull_request_id=pull_request_id,
    )


async def list_repositories() -> list[Repository]:
    """List repositories."""
    return await pull_request_service.list_repositories()


async def get_repository(repository_id: int) -> Repository:
    """Get a repository."""
    return await pull_request_service.get_repository(repository_id=repository_id)


async def delete_repository(repository_id: int) -> None:
    """Delete a repository."""
    return await pull_request_service.delete_repository(repository_id=repository_id)


async def add_repository(
    repository_name: str,
    github_url: str | None = None,
) -> Repository:
    """Add a repository."""
    return await pull_request_service.add_repository(
        repository_name=repository_name,
        github_url=github_url,
    )


async def add_pull_request(
    repository_id: int,
    pull_request_number: int,
) -> PullRequest:
    """Add a pull request."""
    return await pull_request_service.add_pull_request(
        repository_id=repository_id,
        pull_request_number=pull_request_number,
    )


async def get_pull_requests(repository_id: int) -> list[PullRequest]:
    """Get a list of pull requests."""
    return await pull_request_service.get_pull_requests(repository_id=repository_id)


async def get_pull_request(
    repository_id: int,
    pull_request_id: int,
) -> PullRequest:
    """Get a pull request."""
    return await pull_request_service.get_pull_request(
        repository_id=repository_id,
        pull_request_id=pull_request_id,
    )


async def get_reviews(
    repository_id: int,
    pull_request_id: int,
) -> list[Review]:
    """Get a list of reviews."""
    return await pull_request_service.get_reviews(
        repository_id=repository_id,
        pull_request_id=pull_request_id,
    )


async def get_review(
    repository_id: int,
    pull_request_id: int,
    review_id: int,
) -> ReviewResponse:
    """Get a review."""
    return await pull_request_service.get_review(
        repository_id=repository_id,
        pull_request_id=pull_request_id,
        review_id=review_id,
    )


async def delete_review(
    repository_id: int,
    pull_request_id: int,
    review_id: int,
) -> None:
    """Delete a review."""
    return await pull_request_service.delete_review(
        repository_id=repository_id,
        pull_request_id=pull_request_id,
        review_id=review_id,
    )
