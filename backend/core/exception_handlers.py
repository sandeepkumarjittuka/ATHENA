"""Global FastAPI exception handlers."""

from collections.abc import Mapping
from http import HTTPStatus
from typing import TYPE_CHECKING, Any, cast

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from core.exceptions import AthenaError
from core.logging import get_logger
from middleware.request_context import get_request_id

if TYPE_CHECKING:
    from starlette.types import ExceptionHandler

logger = get_logger(__name__)


def register_exception_handlers(application: FastAPI) -> None:
    """Register global exception handlers for API responses."""

    application.add_exception_handler(
        AthenaError,
        cast("ExceptionHandler", athena_error_handler),
    )
    application.add_exception_handler(
        StarletteHTTPException,
        cast("ExceptionHandler", http_exception_handler),
    )
    application.add_exception_handler(
        RequestValidationError,
        cast("ExceptionHandler", validation_error_handler),
    )
    application.add_exception_handler(
        Exception,
        cast("ExceptionHandler", unhandled_exception_handler),
    )


async def athena_error_handler(
    request: Request,
    exc: AthenaError,
) -> JSONResponse:
    """Convert domain/application errors into structured API responses."""

    logger.warning(
        "Application error",
        extra={"path": request.url.path, "error_code": exc.code},
    )
    return error_response(
        status_code=exc.status_code,
        code=exc.code,
        message=exc.message,
    )


async def http_exception_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    """Convert HTTP errors into the standard API error shape."""

    status_code = int(exc.status_code)
    message = str(exc.detail or HTTPStatus(status_code).phrase)
    logger.info(
        "HTTP error",
        extra={"path": request.url.path, "status_code": status_code},
    )
    return error_response(
        status_code=status_code,
        code="http_error",
        message=message,
        headers=exc.headers,
    )


async def validation_error_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Convert request validation errors into the standard API error shape."""

    logger.info(
        "Request validation failed",
        extra={"path": request.url.path, "errors": exc.errors()},
    )
    return error_response(
        status_code=422,
        code="validation_error",
        message="Request validation failed.",
        details=exc.errors(),
    )


async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    """Return a safe response for unhandled exceptions."""

    logger.exception(
        "Unhandled application error",
        extra={"path": request.url.path},
        exc_info=exc,
    )
    return error_response(
        status_code=500,
        code="internal_server_error",
        message="Internal server error.",
    )


def error_response(
    *,
    status_code: int,
    code: str,
    message: str,
    details: Any | None = None,
    headers: Mapping[str, str] | None = None,
) -> JSONResponse:
    """Build the standard API error response body."""

    body: dict[str, Any] = {
        "error": {
            "code": code,
            "message": message,
            "request_id": get_request_id(),
        },
    }
    if details is not None:
        body["error"]["details"] = details

    return JSONResponse(status_code=status_code, content=body, headers=headers)
