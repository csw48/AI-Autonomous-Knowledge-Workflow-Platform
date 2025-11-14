# AI Autonomous Knowledge & Workflow Platform

This repo contains a small but complete AI backend + dashboard used to experiment with RAG, simple agents, and workflow automation. The current milestones cover backend skeleton, document ingestion, search, RAG chat, a basic multi-step agent, tests, CI and Docker stack.

## Repository Layout

- `backend/app` FastAPI application modules (API routes, core config, services, integrations)
- `backend/tests` pytest suite for backend behaviour
- `frontend` Next.js dashboard (health, upload, search, chat)
- `.github/workflows/ci.yml` GitHub Actions pipeline (ruff + pytest)
- `docker-compose.yml` infrastructure for Postgres (pgvector) + API + frontend

## Getting Started

1. Install Poetry: `pip install poetry`.
2. From the repo root run: `poetry install`.
3. (Optional) Activate the venv: `poetry shell`.
4. Launch the API locally: `poetry run uvicorn backend.app.main:app --reload`.
5. Run tests: `poetry run pytest`.
6. Bring up the full stack via Docker:

```bash
docker compose up -d --build
```

This starts:

- `db`: PostgreSQL with the `pgvector` extension (image `ankane/pgvector`).
- `backend`: FastAPI app served via Uvicorn (`http://localhost:8000`).
- `frontend`: Next.js dashboard on `http://localhost:3000`.

## API Endpoints

- `GET /api/v1/health` – readiness probe.
- `POST /api/v1/chat` – simple chat endpoint returning a deterministic stub until a live LLM provider is configured.
- `POST /api/v1/documents` – upload text, PDF, DOCX or image files (multipart) to persist, chunk, OCR (for images) and embed them for RAG/search.

### Search API

- `POST /api/v1/search` – search stored document chunks by substring or vector similarity.

Example:

```bash
curl -X POST http://localhost:8000/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query":"hello","limit":5}'
```

Returns a list of `{ document_id, chunk_index, content }`.

### RAG Chat API

- `POST /api/v1/chat/rag` – retrieval-augmented chat that uses the search service (vector search with keyword fallback) to pull relevant chunks and feed them into the LLM prompt.

Example:

```bash
curl -X POST http://localhost:8000/api/v1/chat/rag \
  -H "Content-Type: application/json" \
  -d '{"query":"What do my notes say about hello world?","top_k":5}'
```

The response contains the LLM `answer` plus the list of `contexts` (document IDs and chunk indices) that backed the answer.

### Agent API

- `POST /api/v1/agents/execute` – simple multi-step agent over stored documents.

Example:

```bash
curl -X POST http://localhost:8000/api/v1/agents/execute \
  -H "Content-Type: application/json" \
  -d '{"goal":"Find info about hello world in my documents","max_chunks":3}'
```

The response contains a final `answer` and a list of `steps` (plan, tool_call, answer) that form a lightweight reasoning trace.

## Configuration

Copy `.env.example` to `.env` and fill in:

- `OPENAI_API_KEY` / `LLM_PROVIDER`
- `DATABASE_URL` / `POSTGRES_*`
- `POSTGRES_PORT`
- `ALLOWED_ORIGINS`
- `VECTOR_DB_URL`
- `NOTION_API_KEY`
- `NOTION_DATABASE_ID`
- `NEXT_PUBLIC_API_BASE_URL`

The `Settings` class in `backend/app/core/config.py` loads them for the FastAPI app. GitHub Actions uses the default dev settings and only runs lint + tests (no external calls).

