"""Pull request services."""

import asyncio

import httpx
from fastapi import HTTPException, status

from api.common.tools.review_pull_request import ReviewPullRequest
from api.config import config
from api.reviewer.dto.responses import ReviewResponse
from api.reviewer.models.pull_request import PullRequest, PullRequestFileChanges
from api.reviewer.models.repository import Repository
from api.reviewer.models.review import Review
from api.reviewer.repositories import pull_request_repository


async def create_review(
    repository_id: int,
    pull_request_id: int,
) -> ReviewResponse:
    """Create a review.

    :param repository_id: The repository id.
    :param pull_request_number: The pull request id.
    :return: The review ID.
    """
    repository = await pull_request_repository.get_repository(
        repository_id=repository_id,
    )
    pull_request = await pull_request_repository.get_pull_request(
        repository_id=repository_id,
        pull_request_id=pull_request_id,
    )

    # TODO: wrap this request in a function
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {config.github_token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    # TODO: support other github urls
    url = f"https://{repository.github_url}/repos/{repository.repository_name}/pulls/{pull_request.pull_request_number}/files"
    timeout = httpx.Timeout(config.request_timeout, read=None)
    async with httpx.AsyncClient() as client:
        try:
            callback = await client.get(
                url,
                headers=headers,
                timeout=timeout,
            )
            callback.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to fetch pull request files from Github.",
            ) from e
        pull_request_files_response = callback.json()

    pull_request_file_changes_requests = [
        PullRequestFileChanges(**file)
        for file in pull_request_files_response
        if set(PullRequestFileChanges.model_fields.keys()).issubset(file.keys())
    ]

    semaphore = asyncio.Semaphore(config.max_concurrent_file_reviews)
    review_tasks = [
        _create_review_task(file_changes=file_changes, semaphore=semaphore)
        for file_changes in pull_request_file_changes_requests
    ]
    review_contents = await asyncio.gather(*review_tasks)

    review = await pull_request_repository.add_review(
        pull_request_id=pull_request_id,
    )

    asyncio.create_task(
        pull_request_repository.add_file_review(
            review_id=review.id,
            review_contents=review_contents,
            file_names=[file.filename for file in pull_request_file_changes_requests],
        ),
    )

    file_names = [file.filename for file in pull_request_file_changes_requests]
    return ReviewResponse(
        review_id=review.id,
        review_contents=review_contents,
        file_names=file_names,
    )


async def _create_review_task(
    file_changes: PullRequestFileChanges,
    semaphore: asyncio.Semaphore,
) -> str:
    """Create a review task for a single file.

    :param file_changes: The pull request file changes.
    :param semaphore: The semaphore.
    :return: The review content.
    """
    answer = ""
    async with semaphore:
        review_content_iterator = await ReviewPullRequest.arun(request=file_changes)

        async for review_content in review_content_iterator:
            answer += review_content

    return answer


async def list_repositories() -> list[Repository]:
    """List repositories."""
    return await pull_request_repository.list_repositories()


async def delete_repository(repository_id: int) -> None:
    """Delete a repository."""
    return await pull_request_repository.delete_repository(repository_id=repository_id)


async def get_repository(repository_id: int) -> Repository:
    """Get a repository."""
    return await pull_request_repository.get_repository(repository_id=repository_id)


async def add_repository(
    repository_name: str,
    github_url: str | None = None,
) -> Repository:
    """Add a repository."""
    return await pull_request_repository.add_repository(
        repository_name=repository_name,
        github_url=github_url,
    )


async def add_pull_request(
    repository_id: int,
    pull_request_number: int,
) -> PullRequest:
    """Add a pull request."""
    return await pull_request_repository.add_pull_request(
        repository_id=repository_id,
        pull_request_number=pull_request_number,
    )


async def get_pull_requests(repository_id: int) -> list[PullRequest]:
    """Get a list of pull requests."""
    return await pull_request_repository.get_pull_requests(repository_id=repository_id)


async def get_pull_request(
    repository_id: int,
    pull_request_id: int,
) -> PullRequest:
    """Get a pull request."""
    return await pull_request_repository.get_pull_request(
        repository_id=repository_id,
        pull_request_id=pull_request_id,
    )


async def get_reviews(
    repository_id: int,
    pull_request_id: int,
) -> list[Review]:
    """Get a list of reviews."""
    return await pull_request_repository.get_reviews(
        repository_id=repository_id,
        pull_request_id=pull_request_id,
    )


async def get_review(
    repository_id: int,
    pull_request_id: int,
    review_id: int,
) -> ReviewResponse:
    """Get a review."""
    return await pull_request_repository.get_review(
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
    return await pull_request_repository.delete_review(
        repository_id=repository_id,
        pull_request_id=pull_request_id,
        review_id=review_id,
    )
