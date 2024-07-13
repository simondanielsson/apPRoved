"""API."""

import logging

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from api.common.routes.general_routes import general_router
from api.reviewer.routes.reviewer_routes import reviewer_router
from api.utils.constants import ApplicationTags
from api.utils.database import init_db

logger = logging.getLogger(__name__)

tags_metadata = [
    {
        "name": ApplicationTags.DEFAULT_TAG,
        "description": "Default operations.",
    },
    {
        "name": ApplicationTags.REVIEWER_TAG,
        "description": "Review PR operations.",
    },
]

api = FastAPI(
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    openapi_tags=tags_metadata,
    redoc_url=None,
    title="apPRoved",
    description="apPRoved API",
    version="0.0.1",
)

api.add_middleware(  # CORS
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.get("/api/{full_path:path}", include_in_schema=False)
async def catch_api_all() -> FileResponse:
    """Return 404 for non-existent api endpoints.

    :return: When we reach this part of the routing precedence, return 404.
    """
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


api.include_router(general_router, tags=["/api"])
api.include_router(reviewer_router, tags=["/api/reviewer"])


@api.on_event("startup")
async def on_startup() -> None:
    """Run hooks on startup."""
    await init_db()
