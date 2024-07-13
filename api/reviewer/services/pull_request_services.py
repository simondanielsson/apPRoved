"""Pull request services."""

import httpx

from api.reviewer.models.review import Review
from api.config import config


async def create_review(
    repository: str,
    pull_request_number: int,
) -> int:
    """Create a review.

    :param repository: The repository name ($OWNER/$REPOSITORY_NAME).
    :param pull_request_number: The pull request number.
    :return: The review ID.
    """

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {config.github_token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    url = f"https://api.github.com/repos/{repository}/pulls/{pull_request_number}/files"
    timeout = httpx.Timeout(config.request_timeout, read=None)
    async with httpx.AsyncClient() as client:
        callback = await client.get(
            url,
            headers=headers,
            timeout=timeout,
        )
        callback.raise_for_status()
        res_json = callback.json()
        print()

    # ask llm to generate review

    # save review in databas
