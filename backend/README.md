# Backend Overview

This FastAPI service is the foundation for the AI Autonomous Knowledge & Workflow Platform. Future milestones will extend it with RAG, agent tooling, MCP-like integrations, and voice support.

## Project Structure

- `app/main.py` application factory and router wiring
- `app/api/routes` endpoint definitions (currently only `health`)
- `app/core` configuration + logging helpers
- `app/services` placeholder for domain services (LLM, RAG, etc.)
- `app/integrations` external service clients (Notion stub in place)
- `tests/` pytest suite

## Development

```bash
poetry install
poetry run uvicorn backend.app.main:app --reload
poetry run pytest
```

## Environment Variables

See `.env.example` for the full list. Key settings today:

- `OPENAI_API_KEY` / `LLM_PROVIDER`
- `DATABASE_URL`
- `VECTOR_DB_URL`
- `NOTION_API_KEY`
- `NOTION_DATABASE_ID`
- `LOG_LEVEL`

The `Settings` class in `backend/app/core/config.py` loads them and exposes defaults for local development.
