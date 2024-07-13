"""Github services."""

import logging

import github

from api.utils.exceptions import ConfigError
from api.config import config

logger = logging.getLogger(__name__)


async def get_github_client() -> github.Github:
    """Get github client."""
    if not config.get("GITHUB_TOKEN"):
        message = (
            "GITHUB_TOKEN not set in environment variables. "
            "This should be set to a valid Github Access Token (fine-grained)"
        )
        raise ConfigError(message)

    access_token = github.Auth.Token(config.GITHUB_TOKEN)
    try:
        github_client = github.Github(auth=access_token)
    except github.BadCredentialsException as e:
        message = (
            "Failed login due to invalid GITHUB_TOKEN. "
            "Please set a valid Github Access Token (fine-grained).",
        )
        raise ConfigError(message) from e

    user = github_client.get_user().login
    logger.info("Authenticated with Github as %s", user)

    return github_client
