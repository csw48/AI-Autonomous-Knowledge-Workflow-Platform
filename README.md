# AI Autonomous Knowledge & Workflow Platform

Initial milestones set up the backend skeleton, basic LLM chat endpoint, test suite, and CI hooks.

## Repository Layout

- `backend/app` FastAPI application modules (API, core config, services, integrations)
- `backend/tests` pytest suite
- `.github/workflows` GitHub Actions pipeline
- `docker-compose.yml` infrastructure for Postgres (pgvector) + API service

## Getting Started

1. Install Poetry (`pip install poetry`).
2. From the repo root run `poetry install`.
3. Activate the virtual environment via `poetry shell` (optional).
4. Launch the API locally: `poetry run uvicorn backend.app.main:app --reload`.
5. Run tests: `poetry run pytest`.

### Run with Docker

```bash
docker compose up --build
```

This starts:

- `db`: PostgreSQL with the `pgvector` extension (image `ankane/pgvector`).
- `backend`: FastAPI app served via Uvicorn (listens on `localhost:8000`).

Override defaults via `.env` or environment variables (`POSTGRES_*`, `DATABASE_URL`).

### API Endpoints

- `GET /api/v1/health` – readiness probe.
- `POST /api/v1/chat` – simple chat endpoint returning a deterministic stub until a live LLM provider is configured.

## Configuration

Copy `.env.example` to `.env` and fill in the environment variables (LLM, database, Notion, etc.). Configuration is powered by `pydantic-settings` and automatically loaded by the FastAPI app.

See `backend/README.md` for backend-specific notes.

### Notion workflow tracking

Set `NOTION_API_KEY` and `NOTION_DATABASE_ID` in `.env` to enable automatic Kanban updates. Update an item manually via:

```bash
poetry run python scripts/notion_update.py "Inicializácia repozitára" Done --note "Tests green"
```

The helper CLI sets the `Status` column and optionally appends notes as Notion comments so every milestone stays in sync with the board.
