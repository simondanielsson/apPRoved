import requests
from fastapi import HTTPException


def create_review(
    repository: str,
    pull_request_number: int,
    github_url: str,
    token: str,
) -> dict:
    api_url = "http://localhost:8082/repositories/{repository_id}/pull_requests/{pull_request_id}/reviews"

    response = requests.post(
        api_url.format(repository_id=0, pull_request_id=0),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
        json={
            "repository": repository,
            "pull_request_number": pull_request_number,
            **({"github_url": github_url} if github_url else {}),
        },
    )

    if response.status_code == 201:
        response_data = response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response_data
