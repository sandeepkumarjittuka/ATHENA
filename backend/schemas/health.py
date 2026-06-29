"""Response schemas for service health endpoints."""

from typing import Literal

from pydantic import BaseModel, ConfigDict

HealthStatus = Literal["ok"]
ReadinessStatus = Literal["ready"]


class HealthResponse(BaseModel):
    """Basic liveness response."""

    status: HealthStatus
    service: str
    version: str
    environment: str

    model_config = ConfigDict(frozen=True)


class ReadinessResponse(BaseModel):
    """Readiness response for infrastructure probes."""

    status: ReadinessStatus
    service: str

    model_config = ConfigDict(frozen=True)
