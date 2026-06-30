"""FastAPI lifespan management."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.types import Lifespan

from application.container import AppContainer
from application.wiring import wire_dependencies
from core.logging import configure_logging, get_logger

logger = get_logger(__name__)


def create_lifespan(container: AppContainer) -> Lifespan[FastAPI]:
    """Create the FastAPI lifespan context manager."""

    @asynccontextmanager
    async def lifespan(application: FastAPI) -> AsyncIterator[None]:
        configure_logging(container.settings)
        wire_dependencies(application, container)
        logger.info(
            "Application startup complete",
            extra={
                "service": container.settings.app_name,
                "version": container.settings.app_version,
                "environment": container.settings.environment,
            },
        )
        try:
            yield
        finally:
            logger.info(
                "Application shutdown complete",
                extra={"service": container.settings.app_name},
            )

    return lifespan
