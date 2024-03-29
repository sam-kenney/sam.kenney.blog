"""Set up the application."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import TYPE_CHECKING

import fastapi
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from static_router import StaticRouter

from src.contentful import Contentful
from src.routes import not_found, router

if TYPE_CHECKING:
    from collections.abc import AsyncIterator


@asynccontextmanager
async def lifespan(app: fastapi.FastAPI) -> AsyncIterator[None]:
    """Set up lifespan variables for the app."""
    content_loader = Contentful("post")
    app.state.static = StaticRouter(content_loader=content_loader)
    app.state.static.register(app)
    app.state.templates = Jinja2Templates("templates")
    yield


def make_app() -> fastapi.FastAPI:
    """Initialise the app."""
    app = fastapi.FastAPI(
        lifespan=lifespan,
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
    )

    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(router)
    app.exception_handler(404)(not_found)

    return app
