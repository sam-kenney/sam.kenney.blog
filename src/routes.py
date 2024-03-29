"""Application routes."""

from __future__ import annotations

from typing import cast

import fastapi
from static_router.models import Page

router = fastapi.APIRouter()


@router.get("/")
def home() -> fastapi.Response:
    """Redirect to blog, maybe I'll do a home one day."""
    return fastapi.responses.RedirectResponse("/blog/")


@router.get("/blog/")
def blog(request: fastapi.Request) -> fastapi.Response:
    """Return the blog page."""
    posts: dict[int, list[Page]] = {}

    for page in request.app.state.static.pages:
        page = cast(Page, page)

        if page.date.year in posts:
            posts[page.date.year].append(page)
        else:
            posts[page.date.year] = [page]

    return request.app.state.templates.TemplateResponse(
        request=request,
        name="blog.html",
        context={
            "request": request,
            "posts": posts,
            "title": "Blog",
        },
    )


@router.get("/projects/")
def projects(request: fastapi.Request) -> fastapi.Response:
    """Return the projects page."""
    return request.app.state.templates.TemplateResponse(
        request=request,
        name="projects.html",
        context={
            "request": request,
        },
    )


def not_found(
    request: fastapi.Request,
    _exception: fastapi.HTTPException,
) -> fastapi.Response:
    """Return the 404 page."""
    return request.app.state.templates.TemplateResponse(
        request=request,
        name="404.html",
        context={"request": request},
    )
