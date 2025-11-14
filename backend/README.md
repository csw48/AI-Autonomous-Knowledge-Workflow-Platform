# Backend Overview

This FastAPI service is the foundation for the AI Autonomous Knowledge & Workflow Platform. It already exposes basic chat, document ingestion, search, and RAG endpoints; future milestones will extend it with agent tooling, MCP-like integrations, and voice support.

## Project Structure

- `app/main.py` application factory and router wiring
- `app/api/routes` endpoint definitions (`health`, `chat`)
- `app/core` configuration + logging helpers
- `app/db` async SQLAlchemy engine/session helpers
- `app/models/db` ORM models (`Document`, `DocumentChunk`)
- `app/services` domain services (LLM stub, `DocumentService`, etc.)
- `app/integrations` external service clients (Notion)
- `tests/` pytest suite

## Development

```bash
poetry install
poetry run uvicorn backend.app.main:app --reload
poetry run pytest
```

## Database & vectors

- Async SQLAlchemy 2.0 stack via `asyncpg`.
- PostgreSQL + `pgvector` is the primary store; local tests fall back to SQLite + JSON embeddings.
- `DocumentService` persists document metadata, chunk text, and embeddings for later retrieval/RAG steps.
- `backend/app/db/session.py` exposes dependency-friendly helpers plus `init_db()`/`close_db()` used by FastAPI lifespan events.

### Docker

`docker-compose.yml` spins up `ankane/pgvector` and the FastAPI container. Ensure `.env` mirrors `.env.example`, then:

```bash
docker compose up --build
```

### API surface

- `GET /api/v1/health` – readiness probe.
- `POST /api/v1/chat` – returns a stubbed LLM answer based on the configured provider. Once API keys are supplied the same abstraction will call the real provider.
- `POST /api/v1/documents` – accepts multipart uploads (currently plaintext) and stores chunked content via `DocumentService` for later embedding/indexing. Response includes generated `id` and the chunk count.

### RAG & search

The backend also wires together:

- `POST /api/v1/search` for keyword/vector search over stored document chunks.
- `POST /api/v1/chat/rag` for retrieval-augmented chat that uses the search service to pull relevant chunks before calling the LLM.

## Environment Variables

See `.env.example` for the full list. Key settings today:

- `OPENAI_API_KEY` / `LLM_PROVIDER`
- `DATABASE_URL` / `POSTGRES_*`
- `POSTGRES_PORT` – host-facing port (default `6543`) if you connect from local tools
- `ALLOWED_ORIGINS`
- `VECTOR_DB_URL`
- `NOTION_API_KEY`
- `NOTION_DATABASE_ID`
- `LOG_LEVEL`

The `Settings` class in `backend/app/core/config.py` loads them and exposes defaults for local development.
