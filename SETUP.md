# Setup

This guide is for developers who want to run RealFarm locally.

## Prerequisites

- Docker Desktop with Compose v2, or separate installations of Python 3.12 and Node.js 20.
- Access to the repository root.
- A copy of `.env.example` renamed to `.env`.

## Recommended setup: Docker Compose

1. Copy the example environment file.

```bash
copy .env.example .env
```

2. Edit `.env` and set at least:

- `JWT_SECRET`
- database passwords
- `WEB_BASE_URL`

3. Start the full stack.

```bash
docker compose up --build
```

If your machine uses the legacy Compose binary, run `docker-compose up --build` instead.

4. Open the services:

- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- API docs: `http://localhost:8000/api/docs`
- MQTT broker: `localhost:1883`
- PostgreSQL: `localhost:5432`

## Local development without Docker

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Simulator

```bash
cd backend/services/simulator
pip install -r requirements.txt
python -m src.main
```

## Validation

Use these checks after making changes.

### Backend

```bash
cd backend
ruff check .
ruff format --check .
python -c "from app.main import app; print('App import OK')"
```

### Frontend

```bash
cd frontend
npm run type-check
npm run lint
npm run build
```

### Simulator

```bash
cd backend/services/simulator
python -c "import src.main; print('Simulator import OK')"
```

## Manual smoke checks

- Log in with the demo account `demo@realfarm.dev` / `demo1234` in development.
- Open the plot and farm views.
- Confirm the API responds at `/api/v1` and `/api/docs`.
- Confirm the simulator publishes telemetry when started.
