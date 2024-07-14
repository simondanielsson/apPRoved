"""Tool to review pull requests."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, AsyncIterator

from api.common.models.message import PromptType
from api.common.tools.tool import get_hydrated_prompt, get_kwarg, get_tool_config_path
from api.utils.constants import Tools
from api.utils.llm import ask_llm

if TYPE_CHECKING:
    from api.reviewer.models.pull_request import PullRequestFileChanges

logger = logging.getLogger(__name__)


class ReviewPullRequest:
    """A tool for reviewing pull requests."""

    tool: Tools = Tools.REVIEW_PULL_REQUEST

    @classmethod
    async def arun(
        cls: type[ReviewPullRequest],
        *args: Any,
        **kwargs: Any,
    ) -> AsyncIterator[str]:
        """Use the tool asynchronously.

        :return: Tool output.
        """
        logger.info(f"Run {cls.tool} tool.")

        request: PullRequestFileChanges = get_kwarg(kwargs, "request")

        template_path = get_tool_config_path(cls.tool)
        system_prompt = get_hydrated_prompt(
            template_path=template_path,
            prompt_type=PromptType.system,
        )
        user_prompt = get_hydrated_prompt(
            template_path=template_path,
            prompt_type=PromptType.user,
            filename=request.filename,
            patch=request.patch,
        )
        return ask_llm(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )
