# AI Autonomous Knowledge & Workflow Platform

Initial milestone for the project: repository bootstrap with backend skeleton and testing scaffold.

## Repository Layout

- `backend/app` FastAPI application modules (API, core config, services, integrations)
- `backend/tests` pytest suite
- `.github/workflows` placeholder for CI flows (to be implemented next milestone)

## Getting Started

1. Install Poetry (`pip install poetry`).
2. From the repo root run `poetry install`.
3. Activate the virtual environment via `poetry shell` (optional).
4. Launch the API locally: `poetry run uvicorn backend.app.main:app --reload`.
5. Run tests: `poetry run pytest`.

## Configuration

Copy `.env.example` to `.env` and fill in the environment variables (LLM, database, Notion, etc.). Configuration is powered by `pydantic-settings` and automatically loaded by the FastAPI app.

See `backend/README.md` for backend-specific notes.
