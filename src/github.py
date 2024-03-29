"""Get projects from GitHub."""

from __future__ import annotations

import os

import httpx
import pydantic
from datetime import datetime


class GitHubProject(pydantic.BaseModel, extra=pydantic.Extra.ignore):
    """Model representing a GitHub project."""

    url: str
    html_url: str
    name: str
    description: str | None = None
    pushed_at: datetime
    archived: bool


class GitHub:
    """Interface with the GitHub REST API."""

    def __init__(self, user: str) -> None:
        """
        Interface with the GitHub REST API.

        Params
        ------
        user: :class:`str`
            The username to interface with the API as.
        """
        self.user = user

        self.http = httpx.AsyncClient(
            base_url=f"https://api.github.com/",
            headers={
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )

    async def close(self) -> None:
        """Close the client."""
        await self.http.aclose()

    async def list_projects(self) -> dict[int, list[GitHubProject]]:
        """List all projects for the given user."""
        response = await self.http.get(
            f"users/{self.user}/repos",
            params={
                "state": "open",
                "per_page": 100,
            }
        )
        response.raise_for_status()

        projects = [GitHubProject(**project) for project in response.json()]
        projects = filter(lambda x: not x.archived, projects)

        res: dict[int, list[GitHubProject]] = {}

        for project in projects:
            if project.pushed_at.year in res:
                res[project.pushed_at.year].append(project)
            else:
                res[project.pushed_at.year] = [project]

        return res
