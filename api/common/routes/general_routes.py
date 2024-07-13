"""General routes."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from api.common.dto.requests import CreateUserRequest
from api.common.dto.responses import TokenResponse, UserResponse
from api.common.models.user import User
from api.common.services import auth_service
from api.common.services.auth_service import get_current_user
from api.utils.constants import ApplicationTags

general_router = APIRouter()

security = HTTPBasic()


@general_router.post(
    "/users",
    tags=[ApplicationTags.DEFAULT_TAG],
)
async def register(
    create_user_request: CreateUserRequest,
) -> JSONResponse:
    """Register a user."""
    if not create_user_request.username or not create_user_request.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username and password are required.",
        )

    await auth_service.create_user(
        username=create_user_request.username,
        password=create_user_request.password,
    )
    response_payload = {"message": "User created successfully."}

    headers = {"Location": "/api/token/"}

    return JSONResponse(
        content=response_payload,
        headers=headers,
        status_code=status.HTTP_201_CREATED,
    )


@general_router.post(
    "/token",
    tags=[ApplicationTags.DEFAULT_TAG],
    response_model=TokenResponse,
)
async def login_for_access_token(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
) -> TokenResponse:
    """Login for an access token."""
    user = await auth_service.authenticate_user(
        username=credentials.username,
        password=credentials.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_service.create_access_token(data={"username": user.username})
    return TokenResponse(access_token=access_token, token_type="bearer")


@general_router.get(
    "/users/me",
    tags=[ApplicationTags.DEFAULT_TAG],
    response_model=UserResponse,
)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserResponse:
    """Read the current user."""
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        is_active=current_user.is_active,
        is_superuser=current_user.is_superuser,
    )
