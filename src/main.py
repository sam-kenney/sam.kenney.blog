"""Example entry point."""

from __future__ import annotations

if __name__ == "__main__":
    import sys

    sys.exit("python -m uvicorn src.main:app --port 8080 --reload")

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING, cast

import fastapi
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from static_router import StaticRouter

from src.contentful import Contentful, Page

if TYPE_CHECKING:
    from collections.abc import AsyncIterator


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI) -> AsyncIterator[None]:
    """Set up lifetime variables for the app."""
    content_loader = Contentful("post")
    app.state.static = StaticRouter(content_loader=content_loader)
    app.state.static.register(app)
    app.state.templates = Jinja2Templates("templates")
    yield


app = fastapi.FastAPI(
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.exception_handler(404)
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


@app.get("/")
def home() -> fastapi.Response:
    """Redirect to blog, maybe I'll do a home one day."""
    return fastapi.responses.RedirectResponse("/blog/")


@app.get("/blog/")
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


@app.get("/projects/")
def projects(request: fastapi.Request) -> fastapi.Response:
    """Return the projects page."""
    return request.app.state.templates.TemplateResponse(
        request=request,
        name="projects.html",
        context={
            "request": request,
        },
    )
