"""Reviewer routes."""

from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
import github
from starlette.status import HTTP_201_CREATED

from api.common.models.user import User
from api.common.services.auth_service import get_current_user
from api.common.services.github_services import get_github_client
from api.reviewer.dto.requests import (
    AddRepositoryRequest,
    CreateReviewRequest,
    RegisterPRRequest,
)
from api.reviewer.models.pull_request import PullRequest
from api.reviewer.models.review import Review
from api.utils.constants import ApplicationTags
from api.reviewer.services import pull_request_services

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
    # TODO: implement
    repository_id = 1

    response_payload = {"repository_id": repository_id, "message": "Repository added."}

    headers = {"Location": f"/repositories/{repository_id}"}
    return JSONResponse(
        content=response_payload,
        headers=headers,
        status_code=HTTP_201_CREATED,
    )


@reviewer_router.post(
    "/repositories/{repository_id}/pull_requests/{pull_request_id}/reviews",
    tags=[ApplicationTags.REVIEWER_TAG],
)
async def create_review(
    repository_id: int,
    pull_request_id: int,
    request: CreateReviewRequest,
    _user: Annotated[User, Depends(get_current_user)],
) -> JSONResponse:
    """Create a review using AI."""
    review_id = await pull_request_services.create_review(
        repository=request.repository,
        pull_request_number=request.pull_request_number,
    )

    response_payload = {"review_id": review_id, "message": "Review created."}

    headers = {"Location": f"/reviews/{review_id}"}

    return JSONResponse(
        content=response_payload,
        headers=headers,
        status_code=HTTP_201_CREATED,
    )


@reviewer_router.get(
    "/pull_requests/{pull_request_id}/reviews",
    tags=[ApplicationTags.REVIEWER_TAG],
)
async def get_reviews(
    pull_request_id: int,
    _user: Annotated[User, Depends(get_current_user)],
) -> list[Review]:
    """Get reviews.

    :param pull_request_id: The pull request ID.
    """
    # TODO: fix path
    return [Review(id=1, pull_request_id=pull_request_id, content="LGTM!")]


@reviewer_router.get("/pull_requests", tags=[ApplicationTags.REVIEWER_TAG])
async def get_pull_requests(
    _user: Annotated[User, Depends(get_current_user)],
) -> list[PullRequest]:
    """Get pull requests."""
    return [
        PullRequest(
            id=2,
            user_id=3,
            title="PR title",
            description="PR description",
            created_at=datetime.now(tz=timezone.utc),
            updated_at=datetime.now(tz=timezone.utc),
        ),
    ]


@reviewer_router.get(
    "/pull_requests/{pull_request_id}",
    tags=[ApplicationTags.REVIEWER_TAG],
)
async def get_pull_request(
    pull_request_id: str,
    _user: Annotated[User, Depends(get_current_user)],
) -> PullRequest:
    """Get a pull request.

    :param pull_request_id: The pull request ID.
    """
    from datetime import datetime

    return PullRequest(
        id=pull_request_id,
        user_id=1,
        title="PR title",
        description="PR description",
        created_at=datetime.now(tz=timezone.utc),
        updated_at=datetime.now(tz=timezone.utc),
    )


@reviewer_router.post("/pull_requests", tags=[ApplicationTags.REVIEWER_TAG])
async def register_pull_request(
    register_pr_request: RegisterPRRequest,
    _user: Annotated[User, Depends(get_current_user)],
) -> JSONResponse:
    """Register a pull request.

    :param pull_request: The pull request.
    """
    if not register_pull_request.pull_request_url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Pull request URL is required.",
        )

    pull_request_id = 1
    response_payload = {"pull_request_id": pull_request_id, "message": "PR registered."}
    headers = {"Location": f"/pull_requests/{pull_request_id}"}
    return JSONResponse(
        content=response_payload,
        headers=headers,
        status_code=status.HTTP_201_CREATED,
    )
