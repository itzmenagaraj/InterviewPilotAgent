# InterviewPilotAgent

InterviewPilotAgent is an interview Q&A assistant that indexes PDF and TXT documents into a FAISS vector store, then answers questions or generates interview-style question-and-answer pairs using Groq LLMs and FastEmbed embeddings.

The project is split into three independently deployable pieces:

- **`agent/`** — the RAG core (document loading, embeddings, FAISS vector store, Groq LLM, prompts) wrapped in its own Flask API. This is the only piece that holds `GROQ_API_KEY`/`HF_TOKEN` and the document/vector-store data. Deploy it on its own host/container, scale it independently, or swap it out entirely without touching the other two pieces.
- **`server/`** — a thin API gateway that the UI talks to. It has no RAG logic of its own; it forwards requests to the agent over HTTP (`AGENT_BASE_URL`) and handles CORS for the UI's origin.
- **`client/`** — a Flask app (Jinja templates + static CSS/JS, same app-factory/blueprint pattern as `agent/`/`server/`) that renders the UI and talks to `server/` over `API_BASE_URL`. New pages are added as a template + a route in `client/app/blueprints/pages.py`.

```
Browser (client/)  --fetch-->  server/ (gateway, CORS)  --HTTP-->  agent/ (RAG + Groq + FAISS)
```

## Requirements

- Python 3.11+
- `GROQ_API_KEY` (and optionally `HF_TOKEN`) for the agent service

## Running locally

Each service has its own `requirements.txt` and `.env`/`.env.example` — install and configure them independently.

### 1. Agent (port 5001)

```bash
cd agent
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env   # then fill in GROQ_API_KEY / HF_TOKEN
python wsgi.py
```

### 2. Server (port 5000)

```bash
cd server
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env   # AGENT_BASE_URL, ALLOWED_ORIGINS
python wsgi.py
```

### 3. Client (port 8000)

```bash
cd client
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
python wsgi.py
```

Open `http://localhost:8000`. Edit `client/static/js/config.js` (`API_BASE_URL`) to point at wherever `server/` is deployed in each environment.

### App workflow

1. Upload PDF or TXT documents in the `Upload Documents` tab.
2. Click `Index Documents` to store document embeddings in FAISS.
3. Ask a question in the `Ask Question` tab to retrieve answers from indexed content.
4. Use the `Generate Q&A` tab to create interview questions and answers for a chosen topic.

## Production deployment

- **agent**: run behind `gunicorn wsgi:app` (already a dependency), keep `GROQ_API_KEY`/`HF_TOKEN` and the `data/` volume private to this service.
- **server**: run behind `gunicorn wsgi:app`, set `AGENT_BASE_URL` to the agent's internal/private address and `ALLOWED_ORIGINS` to the client's public origin.
- **client**: run behind `gunicorn wsgi:app`; only `API_BASE_URL` (in `static/js/config.js`) needs to change per environment.

## Project structure

```
agent/
  core/            # document_loader, embedding_service, vector_store, llm_service, rag_service, prompts, config
  app/              # Flask app factory + blueprints (documents, qa) exposing the agent's HTTP API
  data/             # uploaded documents + FAISS index (agent-local storage)
  wsgi.py, requirements.txt, .env.example

server/
  app/              # Flask app factory + blueprints that forward requests to the agent, CORS config
  wsgi.py, requirements.txt, .env.example

client/
  app/              # Flask app factory + blueprints (pages) rendering the UI
  templates/        # base.html layout + one template per page (index.html)
  static/css/style.css
  static/js/{config.js, app.js}
  wsgi.py, requirements.txt
```

## Notes

- Document chunks are split using a 1000-character window with 150-character overlap.
- The agent's vector store is saved in `agent/data/faiss_db/index.faiss`.
- Embeddings use `BAAI/bge-small-en-v1.5` (FastEmbed) and generation uses `llama-3.3-70b-versatile` (Groq).

## License

This project does not include a license file. Add a license if you plan to share or publish the repository.
