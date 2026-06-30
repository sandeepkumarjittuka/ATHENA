"""Application dependency wiring."""

from fastapi import FastAPI

from application.container import AppContainer
from config.settings import Settings, get_settings


def wire_dependencies(application: FastAPI, container: AppContainer) -> None:
    """Wire process-scoped dependencies into the FastAPI application."""

    def get_settings_override() -> Settings:
        return container.settings

    application.state.container = container
    application.dependency_overrides[get_settings] = get_settings_override
