"""Pull content from contentful."""

from __future__ import annotations

import os
import urllib.parse
from typing import Any

import httpx
import pydantic
from static_router.models import ContentLoader, Page


class Post(pydantic.BaseModel, extra=pydantic.Extra.ignore):
    """Post model."""

    template: str
    date: str
    title: str
    content: str


class Contentful(ContentLoader):
    """Load static content from Contentful."""

    def __init__(
        self,
        content_type: str,
        *,
        content_model: type[Post] = Post,
        contentful_space: str | None = None,
        contentful_token: str | None = None,
        api: str = "cdn",
    ) -> None:
        """
        Load static content from Contentful.

        Params
        ------
        content_type: :class:`str`
            The content type in contentful to retrieve.

        content_model: :class:`type[Post]`
            A pydantic model representing the content model \
            in Contentful.

        contentful_space: :class:`str | None`
            The contentful space ID. Can be inferred from \
            the `CONTENTFUL_SPACE` environment variable.

        contentful_token: :class:`str | None`
            The contentful auth token. Can be inferred from \
            the `CONTENTFUL_TOKEN` environment variable.
        """
        token = os.environ.get("CONTENTFUL_TOKEN", contentful_token)
        space = os.environ.get("CONTENTFUL_SPACE", contentful_space)

        if not token:
            raise ValueError("Token must be provided")

        if not space:
            raise ValueError("Space must be provided")

        self.content_type = content_type
        self.content_model = content_model
        self.token = token
        self.url = (
            f"https://{api}.contentful.com/spaces/{space}/environments/master/entries"
        )

    def load(self) -> list[Page]:
        """Load the content."""
        posts = self._load_as_model()

        template = """
        ---
        template: {post.template}
        date: {post.date}
        title: {post.title}
        ---
        {post.content}
        """

        return [
            Page.from_markdown_string(
                template.format(post=post),
                path=urllib.parse.quote(
                    f"/blog/{post.title.lower().replace(' ', '-')}",
                ),
            )
            for post in posts
        ]

    def _load_as_model(self) -> list[Post]:
        """Load content from Contentful as the specified model."""
        content = self._get_content()
        return [self.content_model(**row["fields"]) for row in content]

    def _get_content(self) -> list[dict[str, Any]]:
        """Get the content from Contentful."""
        response = httpx.get(
            f"{self.url}",
            headers={
                "Accept": "application/json",
                "Authorization": f"Bearer {self.token}",
            },
            params={
                "content_type": self.content_type,
            },
        )

        response.raise_for_status()
        return response.json()["items"]
