# Server

A thin API gateway between the `client/` UI and the `agent/` RAG service. It has no RAG logic of its own — it forwards requests to `agent/` over HTTP and handles CORS for the client's origin.

## Endpoints

Mirrors the agent's API and proxies to it:

- `POST /api/documents/upload` → `agent/api/documents/upload`
- `POST /api/qa/answer` → `agent/api/qa/answer`
- `POST /api/qa/generate` → `agent/api/qa/generate`
- `GET /health`

Returns `502 {"error": "Agent service is unavailable"}` if the agent can't be reached.

## Setup

```bash
cd server
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env`:

```
AGENT_BASE_URL=http://localhost:5001
ALLOWED_ORIGINS=http://localhost:8000
```

`ALLOWED_ORIGINS` is a comma-separated list of origins allowed to call this API (CORS). `localhost` and `127.0.0.1` are treated as different origins by browsers — include both if the client might be opened either way, e.g. `http://localhost:8000,http://127.0.0.1:8000`.

## Run

The agent must be running first (see `agent/README.md`).

```bash
python wsgi.py
```

Runs on `http://localhost:5000`.

For production, run behind a WSGI server instead, with `AGENT_BASE_URL` set to the agent's internal/private address and `ALLOWED_ORIGINS` set to the client's public origin:

```bash
gunicorn wsgi:app -b 0.0.0.0:5000
```
