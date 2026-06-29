"""Tests for backend health endpoints."""

from fastapi.testclient import TestClient

from app.main import create_app
from config.settings import Settings


def test_health_check_returns_service_metadata() -> None:
    """Health endpoint should expose basic service metadata."""

    settings = Settings(environment="testing", debug=True)
    client = TestClient(create_app(settings))

    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "ATHENA",
        "version": "0.1.0",
        "environment": "testing",
    }


def test_readiness_check_returns_ready_status() -> None:
    """Readiness endpoint should confirm the API process can respond."""

    settings = Settings(environment="testing", debug=True)
    client = TestClient(create_app(settings))

    response = client.get("/api/v1/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ready", "service": "ATHENA"}
