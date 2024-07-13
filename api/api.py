"""API."""

import logging

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

logger = logging.getLogger(__name__)

tags_metadata = [
    {
        "name": "gateway",
        "description": "Gateway endpoints.",
    },
    {
        "name": "reviewer",
        "description": "PR reviewer endpoints.",
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
