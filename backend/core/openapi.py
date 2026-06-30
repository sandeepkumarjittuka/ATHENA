"""OpenAPI configuration helpers."""

from typing import Any

from config.settings import Settings

OPENAPI_TAGS: list[dict[str, str]] = [
    {
        "name": "health",
        "description": "Operational liveness and readiness endpoints.",
    },
]


def build_openapi_config(settings: Settings) -> dict[str, Any]:
    """Build FastAPI OpenAPI and documentation configuration."""

    docs_enabled = settings.debug
    return {
        "title": settings.app_name,
        "summary": "AI-powered market intelligence and decision support API.",
        "description": (
            "ATHENA analyzes market structure, indicators, news, sentiment, "
            "volatility, liquidity, sector strength, and risk. ATHENA never "
            "executes trades automatically."
        ),
        "version": settings.app_version,
        "debug": settings.debug,
        "docs_url": "/docs" if docs_enabled else None,
        "redoc_url": "/redoc" if docs_enabled else None,
        "openapi_url": "/openapi.json",
        "openapi_tags": OPENAPI_TAGS,
        "contact": {"name": "ATHENA Team"},
        "license_info": {"name": "MIT"},
        "servers": [
            {
                "url": settings.api_prefix,
                "description": "Version 1 API",
            },
        ],
    }
