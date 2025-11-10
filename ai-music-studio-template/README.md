
# AI Music Studio – Starter Template (Next.js + FastAPI)

This template gives you a **ready-to-hack** project that:
- Generates lyrics (stubbed)
- Composes instrumental tracks (stubbed)
- Strips vocals (stubbed)
- Reintegrates vocals (stubbed)
- Exports audio and supports a simple feedback loop

**Stack**
- Frontend: Next.js (App Router) + Tailwind, simple multitab UI
- Backend: FastAPI with endpoints and in-memory "job" queue
- Storage: S3-compatible stub (local temp) – swap for MinIO/S3 later

## Quick Start

### 1) Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2) Frontend
```bash
cd ../frontend
npm i
cp ../.env.example .env.local
npm run dev
```

Open http://localhost:3000

## Endpoints
- POST `/v1/lyrics.generate`
- POST `/v1/compose.generate`
- POST `/v1/separate.vocals`
- POST `/v1/mix.reintegrate`
- GET  `/v1/jobs/{id}/status`
- GET  `/v1/projects/{id}`
- POST `/v1/feedback`

All endpoints are **stubbed** for fast iteration; wire actual ML/DSP later.

## Notes
- Replace the stubs in `backend/app/services/` with real model calls.
- Use proper object storage (MinIO/S3) in production.
- The UI is intentionally minimal. Extend `app/(studio)/page.tsx` and components.
