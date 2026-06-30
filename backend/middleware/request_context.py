"""Request context storage."""

from contextvars import ContextVar, Token

REQUEST_ID_UNAVAILABLE = "-"

_request_id: ContextVar[str] = ContextVar(
    "request_id",
    default=REQUEST_ID_UNAVAILABLE,
)


def get_request_id() -> str:
    """Return the current request ID."""

    return _request_id.get()


def set_request_id(request_id: str) -> Token[str]:
    """Store a request ID in the current context."""

    return _request_id.set(request_id)


def reset_request_id(token: Token[str]) -> None:
    """Reset the request ID context variable."""

    _request_id.reset(token)
