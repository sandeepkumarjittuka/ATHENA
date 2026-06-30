"""Request correlation middleware."""

import time
from uuid import uuid4

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

from core.logging import get_logger
from middleware.request_context import reset_request_id, set_request_id

logger = get_logger(__name__)


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Attach a correlation ID to each HTTP request."""

    def __init__(self, app: ASGIApp, *, header_name: str) -> None:
        super().__init__(app)
        self.header_name = header_name

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        """Process an HTTP request with request ID context."""

        request_id = request.headers.get(self.header_name, uuid4().hex)
        token = set_request_id(request_id)
        started_at = time.perf_counter()

        try:
            response = await call_next(request)
        finally:
            duration_ms = round((time.perf_counter() - started_at) * 1000, 2)
            logger.info(
                "HTTP request completed",
                extra={
                    "method": request.method,
                    "path": request.url.path,
                    "duration_ms": duration_ms,
                },
            )
            reset_request_id(token)

        response.headers[self.header_name] = request_id
        response.headers["X-Process-Time-Ms"] = str(duration_ms)
        return response
