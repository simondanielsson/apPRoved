"""Reviewer routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.status import HTTP_201_CREATED

from api.common.models.user import User
from api.common.services.auth_service import get_current_user
from api.reviewer.controllers import pull_request_controller
from api.reviewer.dto.requests import (
    AddRepositoryRequest,
    RegisterPRRequest,
)
from api.reviewer.dto.responses import ReviewResponse
from api.reviewer.models.pull_request import PullRequest
from api.reviewer.models.repository import Repository
from api.reviewer.models.review import Review
from api.utils.constants import ApplicationTags

reviewer_router = APIRouter()


@reviewer_router.post(
    "/repositories",
    tags=[ApplicationTags.REVIEWER_TAG],
    status_code=HTTP_201_CREATED,
)
async def add_repository(
    request: AddRepositoryRequest,
    _user: Annotated[User, Depends(get_current_user)],
) -> JSONResponse:
    """Register a repository."""
    repository = await pull_request_controller.add_repository(
        repository_name=request.repository_name,
        github_url=request.github_url,
    )
    response_payload = {"repository_id": repository.id, "message": "Repository added."}

    headers = {"Location": f"/repositories/{repository.id}"}
    return JSONResponse(
        content=response_payload,
        headers=headers,
        status_code=HTTP_201_CREATED,
    )


@reviewer_router.get(
    "/repositories",
    tags=[ApplicationTags.REVIEWER_TAG],
    status_code=status.HTTP_200_OK,
)
async def list_repositories(
    _user: Annotated[User, Depends(get_current_user)],
) -> list[Repository]:
    """List repositories."""
    return await pull_request_controller.list_repositories()


@reviewer_router.delete(
    "/repositories/{repository_id}",
    tags=[ApplicationTags.REVIEWER_TAG],
    status_code=status.HTTP_200_OK,
)
async def delete_repository(
    repository_id: int,
    _user: Annotated[User, Depends(get_current_user)],
) -> JSONResponse:
    """Delete a repository."""
    await pull_request_controller.delete_repository(repository_id=repository_id)

    return JSONResponse(
        content={"message": "Repository deleted."},
        status_code=status.HTTP_204_NO_CONTENT,
    )


@reviewer_router.get(
    "/repositories/{repository_id}",
    tags=[ApplicationTags.REVIEWER_TAG],
    status_code=status.HTTP_200_OK,
)
async def get_repository(
    repository_id: int,
    _user: Annotated[User, Depends(get_current_user)],
) -> Repository:
    """Get a repository.

    :param repository_id: The repository ID.
    """
    return await pull_request_controller.get_repository(repository_id=repository_id)


@reviewer_router.get(
    "/repositories/{repository_id}/pull_requests",
    tags=[ApplicationTags.REVIEWER_TAG],
)
async def get_pull_requests(
    repository_id: int,
    _user: Annotated[User, Depends(get_current_user)],
) -> list[PullRequest]:
    """Get pull requests."""
    return await pull_request_controller.get_pull_requests(repository_id=repository_id)


@reviewer_router.get(
    "repositories/{repository_id}/pull_requests/{pull_request_id}",
    tags=[ApplicationTags.REVIEWER_TAG],
)
async def get_pull_request(
    repository_id: int,
    pull_request_id: int,
    _user: Annotated[User, Depends(get_current_user)],
) -> PullRequest:
    """Get a pull request.

    :param pull_request_id: The pull request ID.
    """
    return await pull_request_controller.get_pull_request(
        repository_id=repository_id,
        pull_request_id=pull_request_id,
    )


@reviewer_router.post(
    "/repositories/{repository_id}/pull_requests",
    tags=[ApplicationTags.REVIEWER_TAG],
)
async def register_pull_request(
    repository_id: int,
    request: RegisterPRRequest,
    _user: Annotated[User, Depends(get_current_user)],
) -> JSONResponse:
    """Register a pull request.

    :param pull_request: The pull request.
    """
    if not request.pull_request_number:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Pull repository id is required.",
        )

    pull_request = await pull_request_controller.add_pull_request(
        repository_id=repository_id,
        pull_request_number=request.pull_request_number,
    )

    response_payload = {"pull_request_id": pull_request.id, "message": "PR registered."}
    headers = {"Location": f"/pull_requests/{pull_request.id}"}
    return JSONResponse(
        content=response_payload,
        headers=headers,
        status_code=status.HTTP_201_CREATED,
    )


@reviewer_router.get(
    "/repositories/{repository_id}/pull_requests/{pull_request_id}/reviews",
    tags=[ApplicationTags.REVIEWER_TAG],
)
async def get_reviews(
    repository_id: int,
    pull_request_id: int,
    _user: Annotated[User, Depends(get_current_user)],
) -> list[Review]:
    """Get reviews.

    :param pull_request_id: The pull request ID.
    """
    return await pull_request_controller.get_reviews(
        repository_id=repository_id,
        pull_request_id=pull_request_id,
    )


@reviewer_router.get(
    "/repositories/{repository_id}/pull_requests/{pull_request_id}/reviews/{review_id}",
    tags=[ApplicationTags.REVIEWER_TAG],
    status_code=status.HTTP_200_OK,
)
async def get_review(
    repository_id: int,
    pull_request_id: int,
    review_id: int,
) -> ReviewResponse:
    """Get a review."""
    return await pull_request_controller.get_review(
        repository_id=repository_id,
        pull_request_id=pull_request_id,
        review_id=review_id,
    )


@reviewer_router.delete(
    "/repositories/{repository_id}/pull_requests/{pull_request_id}/reviews/{review_id}",
    tags=[ApplicationTags.REVIEWER_TAG],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_review(
    repository_id: int,
    pull_request_id: int,
    review_id: int,
    _user: Annotated[User, Depends(get_current_user)],
) -> JSONResponse:
    """Delete a review."""
    await pull_request_controller.delete_review(
        repository_id=repository_id,
        pull_request_id=pull_request_id,
        review_id=review_id,
    )

    return JSONResponse(
        content={"message": "Review deleted."},
        status_code=status.HTTP_204_NO_CONTENT,
    )


@reviewer_router.post(
    "/repositories/{repository_id}/pull_requests/{pull_request_id}/reviews",
    tags=[ApplicationTags.REVIEWER_TAG],
)
async def create_review(
    repository_id: int,
    pull_request_id: int,
    _user: Annotated[User, Depends(get_current_user)],
) -> JSONResponse:
    """Create a review using AI."""
    review_response: ReviewResponse = await pull_request_controller.create_review(
        repository_id=repository_id,
        pull_request_id=pull_request_id,
    )

    response_payload = {
        "review_contents": review_response.review_contents,
        "review_id": review_response.review_id,
        "message": "Review created.",
    }

    headers = {"Location": f"/reviews/{review_response.review_id}"}

    return JSONResponse(
        content=response_payload,
        headers=headers,
        status_code=HTTP_201_CREATED,
    )
