# syntax=docker/dockerfile:1.7

ARG PYTHON_VERSION=3.13

# ---------- Builder: create the virtual environment ----------
FROM ghcr.io/astral-sh/uv:python${PYTHON_VERSION}-bookworm-slim AS builder

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install runtime dependencies first to leverage Docker layer caching.
COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv uv sync --frozen --no-dev

# ---------- Runtime ----------
FROM python:${PYTHON_VERSION}-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/app/.venv/bin:$PATH"

# Non-root user for the application process.
RUN groupadd --system app \
    && useradd --system --gid app --create-home app

WORKDIR /app

# Virtual environment from builder (read-only is fine at runtime).
COPY --from=builder --chown=app:app /app/.venv /app/.venv
# Application source.
COPY --chown=app:app . .

USER app

EXPOSE 8000

# TCP-level liveness check (does not depend on any HTTP route existing yet).
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import socket; socket.create_connection(('127.0.0.1', 8000), 2).close()" || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
