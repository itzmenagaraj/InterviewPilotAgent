# Agent

The RAG core: document loading, chunking, embeddings, FAISS vector store, and Groq LLM calls, wrapped in a Flask API. This is the only piece that holds `GROQ_API_KEY`/`HF_TOKEN` and the document/vector-store data.

## Endpoints

- `POST /api/documents/upload` — multipart upload (`files`, PDF/TXT), chunks and indexes them into FAISS
- `POST /api/qa/answer` — `{"question": "..."}` → retrieves context and answers via Groq
- `POST /api/qa/generate` — `{"topic": "...", "difficulty": "Beginner|Intermediate|Advanced", "count": 1-50}` → generates interview Q&A pairs
- `GET /health`

## Setup

```bash
cd agent
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env`:

```
GROQ_API_KEY=your_groq_api_key_here
HF_TOKEN=your_huggingface_token_here   # only needed if the embedding model requires auth
```

## Run

```bash
python wsgi.py
```

Runs on `http://localhost:5001`. First startup takes ~20-30s while the embedding model loads.

For production, run behind a WSGI server instead:

```bash
gunicorn wsgi:app -b 0.0.0.0:5001
```

## Notes

- Uploaded files land in `data/documents/`; the FAISS index is persisted to `data/faiss_db/`. Both are created automatically on startup.
- Chunking: 1000-character window, 150-character overlap (`core/config.py`).
- Embeddings: `BAAI/bge-small-en-v1.5` (FastEmbed). Generation: `llama-3.3-70b-versatile` (Groq).
- Keep this service private — it holds API keys and should not be exposed directly to the browser. `server/` is the public-facing gateway.
