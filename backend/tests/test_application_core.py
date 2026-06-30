"""Tests for ATHENA application core behavior."""

from fastapi import APIRouter
from fastapi.testclient import TestClient

from app.main import create_app
from config.settings import Settings
from core.exceptions import AthenaError


def test_openapi_configuration_uses_application_metadata() -> None:
    """OpenAPI should expose ATHENA API metadata."""

    settings = Settings(environment="testing", debug=True)
    client = TestClient(create_app(settings))

    response = client.get("/openapi.json")

    assert response.status_code == 200
    payload = response.json()
    assert payload["info"]["title"] == "ATHENA"
    assert payload["info"]["version"] == "0.1.0"
    assert payload["servers"] == [{"url": "/api/v1", "description": "Version 1 API"}]


def test_global_exception_handler_returns_standard_error_shape() -> None:
    """Expected application errors should use the global error envelope."""

    settings = Settings(environment="testing", debug=True)
    app = create_app(settings)
    router = APIRouter()

    @router.get("/expected-error")
    async def expected_error() -> None:
        raise AthenaError(
            "Expected failure.",
            code="expected_failure",
            status_code=409,
        )

    app.include_router(router, prefix=settings.api_prefix)
    client = TestClient(app)

    response = client.get("/api/v1/expected-error", headers={"X-Request-ID": "abc"})

    assert response.status_code == 409
    assert response.json() == {
        "error": {
            "code": "expected_failure",
            "message": "Expected failure.",
            "request_id": "abc",
        }
    }
