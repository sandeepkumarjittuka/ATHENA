"""FastAPI dependency helpers."""

from typing import Annotated, cast

from fastapi import Depends, Request

from application.container import AppContainer
from config.settings import Settings


def get_container(request: Request) -> AppContainer:
    """Return the application dependency container."""

    return cast("AppContainer", request.app.state.container)


ContainerDependency = Annotated[AppContainer, Depends(get_container)]


def get_app_settings(container: ContainerDependency) -> Settings:
    """Return application settings from the dependency container."""

    return container.settings


SettingsDependency = Annotated[Settings, Depends(get_app_settings)]
