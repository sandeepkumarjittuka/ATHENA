# ATHENA

Project repository for ATHENA.

## Structure

- `docs/` - Documentation files
- `backend/` - Backend services
- `frontend/` - Frontend application
- `agents/` - Agent modules
- `database/` - Database schemas and migrations
- `infrastructure/` - Infrastructure as Code
- `deployment/` - Deployment configurations
- `tests/` - Test suites
- `scripts/` - Utility scripts

## Backend Foundation

The backend exposes a FastAPI ASGI app at `backend/app/main.py`.

Initial operational endpoints:

- `GET /api/v1/health` - service liveness metadata
- `GET /api/v1/ready` - readiness probe

Local backend setup:

```powershell
cd backend
uv sync
uv run uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Backend verification:

```powershell
uv run pytest
uv run ruff check .
uv run black --check .
uv run mypy .
```

Docker files are located in `backend/`. Docker Desktop requires WSL on
Windows before `docker compose up` can start Linux containers.
