# Frontend UI

Simple Next.js dashboard to exercise backend endpoints and visualize status.

## Setup

```bash
cd frontend
npm install
cp .env.local.example .env.local
```

Update `NEXT_PUBLIC_API_BASE_URL` if your backend is not running on `http://localhost:8000`.

## Commands

- `npm run dev` - start dev server on http://localhost:3000 (use `cmd /c npm run dev` from PowerShell if execution policy blocks npm).
- `npm run lint` - ESLint via Next.js.
- `npm run test` - Vitest + Testing Library coverage for the health + chat panels.
- `npm run build` - production build sanity check.

## Docker

The included Dockerfile builds a production image that `docker compose` uses. From the repo root run:

```bash
docker compose up -d --build
```

This launches Postgres, the FastAPI backend (port 8000), and this frontend (port 3000) serving the production Next.js build. Ensure `NEXT_PUBLIC_API_BASE_URL` is set before building so the container points at the correct backend URL.

## Features

- **HealthStatus** card polling `/api/v1/health` every 30s and manual refresh button.
- **ChatPanel** that hits `/api/v1/chat`, preserves a local response history, and surfaces provider name + answer.
- React Query providers wrapped globally for caching + automatic retries.
- Dark dashboard styling in `app/globals.css` for quick visual feedback.
