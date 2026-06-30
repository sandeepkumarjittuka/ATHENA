"""Health and readiness endpoints."""

from fastapi import APIRouter

from application.dependencies import SettingsDependency
from schemas.health import HealthResponse, ReadinessResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check(settings: SettingsDependency) -> HealthResponse:
    """Return service liveness metadata."""

    return HealthResponse(
        status="ok",
        service=settings.app_name,
        version=settings.app_version,
        environment=settings.environment,
    )


@router.get("/ready", response_model=ReadinessResponse)
async def readiness_check(settings: SettingsDependency) -> ReadinessResponse:
    """Return service readiness status."""

    return ReadinessResponse(status="ready", service=settings.app_name)
