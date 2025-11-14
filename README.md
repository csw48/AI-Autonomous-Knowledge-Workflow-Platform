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
6. (Optional) Bring up Postgres + API via Docker: `docker compose up -d --build`.

### Run with Docker

```bash
docker compose up --build
```

This starts:

- `db`: PostgreSQL with the `pgvector` extension (image `ankane/pgvector`).
- `backend`: FastAPI app served via Uvicorn (listens on `localhost:8000`).
- `frontend`: Next.js dashboard (production `next start`) exposed on `http://localhost:3000`.
- Containers auto-initialize the schema with retry logic so you can immediately hit `/api/v1/*` and see the UI update live.

Override defaults via `.env` or environment variables (`POSTGRES_*`, `DATABASE_URL`).

### API Endpoints

- `GET /api/v1/health` – readiness probe.
- `POST /api/v1/chat` – simple chat endpoint returning a deterministic stub until a live LLM provider is configured.
- `POST /api/v1/documents` – upload plaintext files (multipart) to persist and pre-chunk them for RAG ingestion.

### Document ingestion

Example `curl`:

```bash
curl -X POST http://localhost:8000/api/v1/documents \
  -F "file=@notes.txt" \
  -F "title=Notes from standup"
```

The backend currently accepts UTF-8/Latin-1 text, chunks it server-side (800 chars with overlap), generates stub embeddings, and stores everything for later RAG and search.

## Configuration

Copy `.env.example` to `.env` and fill in the environment variables (LLM, database, Notion, etc.). Configuration is powered by `pydantic-settings` and automatically loaded by the FastAPI app.

See `backend/README.md` for backend-specific notes.

Key variables:

- `OPENAI_API_KEY` / `LLM_PROVIDER`
- `DATABASE_URL` / `POSTGRES_*`
- `POSTGRES_PORT` (default `6543` exposed to host for local tools)
- `ALLOWED_ORIGINS` (comma-separated domains allowed to call the API; defaults to `http://localhost:3000`)
- `VECTOR_DB_URL`
- `NOTION_API_KEY`
- `NOTION_DATABASE_ID`
- `NEXT_PUBLIC_API_BASE_URL` (consumed by the frontend)

### Notion workflow tracking

Set `NOTION_API_KEY` and `NOTION_DATABASE_ID` in `.env` to enable automatic Kanban updates. Update an item manually via:

```bash
poetry run python scripts/notion_update.py "Inicializácia repozitára" Done --note "Tests green"
```

The helper CLI sets the `Status` column and optionally appends notes as Notion comments so every milestone stays in sync with the board.

## Frontend dashboard

- `cd frontend && npm install`
- Copy `.env.local.example` to `.env.local` (defaults to `http://localhost:8000`).
- Start dev server: `cmd /c npm run dev` (PowerShell users can also run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` then `npm run dev`).
- Tests: `npm run test` (Vitest + RTL), lint: `npm run lint`, production build check: `npm run build`.

When the backend containers are up (`localhost:8000`), navigating to `http://localhost:3000` shows:

- Health card polling `/api/v1/health` every 30s.
- Chat panel hitting `/api/v1/chat` and displaying stubbed responses/history.
- Document upload card that posts plaintext files to `/api/v1/documents` and shows upload results live.

## CI/CD

GitHub Actions (`.github/workflows/ci.yml`) runs on every push/PR to lint (`ruff`) and test (`pytest`) the backend. Frontend lint/tests run locally today and will be added to CI in an upcoming milestone.


### Search API

- `POST /api/v1/search` – search stored document chunks by substring. Example:

```bash
curl -X POST http://localhost:8000/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query":"hello","limit":5}'
```

Results return a list of `{ document_id, chunk_index, content }`.

### RAG Chat API

- `POST /api/v1/chat/rag` �?" retrieval-augmented chat that uses the search service (vector search with keyword fallback) to pull relevant chunks and feed them into the LLM prompt.

Example:

```bash
curl -X POST http://localhost:8000/api/v1/chat/rag \
  -H "Content-Type: application/json" \
  -d '{"query":"What do my notes say about hello world?","top_k":5}'
```

The response contains the LLM `answer` plus the list of `contexts` (document IDs and chunk indices) that backed the answer.
