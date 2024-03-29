"""Example entry point."""

from __future__ import annotations

if __name__ == "__main__":
    import sys

    sys.exit("python -m uvicorn src.main:app --port 8080 --reload")

import fastapi
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from static_router import StaticRouter

from src.contentful import Contentful, Page

app = fastapi.FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)
app.mount("/static", StaticFiles(directory="static"), name="static")

content_loader = Contentful(content_type="post")
static = StaticRouter(content_loader=content_loader)
static.register(app)


@app.exception_handler(404)
def not_found(
    request: fastapi.Request,
    _exception: fastapi.HTTPException,
) -> fastapi.Response:
    """Return the 404 page."""
    templates = Jinja2Templates("templates")

    return templates.TemplateResponse(
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
    templates = Jinja2Templates("templates")

    posts: dict[int, list[Page]] = {}

    for post in static.pages:
        if post.date.year in posts:
            posts[post.date.year].append(post)
        else:
            posts[post.date.year] = [post]

    return templates.TemplateResponse(
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
    templates = Jinja2Templates("templates")
    return templates.TemplateResponse(
        request=request,
        name="projects.html",
        context={
            "request": request,
        },
    )
