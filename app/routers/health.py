"""Health check endpoints."""

import logging
import time
from datetime import datetime

from fastapi import APIRouter, status
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["health"])

# Application start time
START_TIME = time.time()


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    uptime_seconds: float
    version: str = "0.1.0"


class ReadyResponse(BaseModel):
    status: str
    checks: dict


@router.get(
    "/",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Basic health check",
)
async def health_check():
    """Returns basic health status."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        uptime_seconds=round(time.time() - START_TIME, 2),
    )


@router.get(
    "/ready",
    response_model=ReadyResponse,
    status_code=status.HTTP_200_OK,
    summary="Readiness probe",
)
async def readiness_check():
    """Returns readiness status with dependency checks."""
    checks = {
        "app": "ok",
    }

    # Add database check if configured
    # checks["database"] = await check_database()

    all_ok = all(v == "ok" for v in checks.values())

    return ReadyResponse(
        status="ready" if all_ok else "not_ready",
        checks=checks,
    )


@router.get(
    "/metrics",
    status_code=status.HTTP_200_OK,
    summary="Prometheus-compatible metrics",
)
async def metrics():
    """Returns basic metrics in Prometheus format."""
    uptime = time.time() - START_TIME
    metrics_data = f"""# HELP app_uptime_seconds Application uptime in seconds
# TYPE app_uptime_seconds gauge
app_uptime_seconds {uptime}

# HELP app_info Application information
# TYPE app_info gauge
app_info{{version="0.1.0"}} 1
"""
    return metrics_data
