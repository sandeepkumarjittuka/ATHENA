"""FastAPI application factory and ASGI entrypoint."""

from fastapi import FastAPI

from api.router import api_router
from config.settings import Settings, get_settings


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure the ATHENA FastAPI application."""

    app_settings = settings or get_settings()

    application = FastAPI(
        title=app_settings.app_name,
        version=app_settings.app_version,
        debug=app_settings.debug,
        docs_url="/docs" if app_settings.debug else None,
        redoc_url="/redoc" if app_settings.debug else None,
    )

    def get_app_settings_override() -> Settings:
        return app_settings

    application.dependency_overrides[get_settings] = get_app_settings_override
    application.include_router(api_router, prefix=app_settings.api_prefix)

    return application


app = create_app()
