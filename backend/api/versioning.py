"""API versioning configuration."""

from fastapi import FastAPI

from api.router import api_router
from config.settings import Settings


def include_versioned_api(application: FastAPI, settings: Settings) -> None:
    """Attach all versioned API routers to the application."""

    application.include_router(api_router, prefix=settings.api_prefix)
