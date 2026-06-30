"""FastAPI application factory and ASGI entrypoint."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.versioning import include_versioned_api
from application.container import AppContainer
from application.wiring import wire_dependencies
from config.settings import Settings, get_settings
from core.exception_handlers import register_exception_handlers
from core.lifespan import create_lifespan
from core.logging import configure_logging
from core.openapi import build_openapi_config
from middleware.request_id import RequestIdMiddleware


def create_app(settings: Settings | None = None) -> FastAPI:
    """Create and configure the ATHENA FastAPI application."""

    app_settings = settings or get_settings()
    container = AppContainer(settings=app_settings)
    configure_logging(app_settings)

    application = FastAPI(
        **build_openapi_config(app_settings),
        lifespan=create_lifespan(container),
    )

    wire_dependencies(application, container)
    register_exception_handlers(application)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=app_settings.cors_allow_origins,
        allow_methods=app_settings.cors_allow_methods,
        allow_headers=app_settings.cors_allow_headers,
    )
    application.add_middleware(
        RequestIdMiddleware,
        header_name=app_settings.request_id_header,
    )

    include_versioned_api(application, app_settings)

    return application


app = create_app()
