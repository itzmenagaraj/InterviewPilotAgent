# InterviewPilotAgent

InterviewPilotAgent is a Streamlit-based interview Q&A assistant that indexes PDF and TXT documents into a FAISS vector store, then answers questions or generates interview-style question-and-answer pairs using Groq LLMs and HuggingFace embeddings.

## Features

- Upload PDF or TXT documents through a Streamlit UI
- Index documents into a local FAISS vector store
- Ask interview questions based on document context
- Generate topic-based interview Q&A pairs with difficulty control
- Stores uploaded documents and vector index under `data/`

## Requirements

- Python 3.11+
- `GROQ_API_KEY` environment variable configured in a `.env` file
- Dependencies listed in `requirements.txt`

## Installation

1. Clone the repository

```bash
git clone https://github.com/<your-org>/InterviewPilotAgent.git
cd InterviewPilotAgent
```

2. Create and activate a Python environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Add your Groq API key to a `.env` file

```text
GROQ_API_KEY=your_groq_api_key_here
```

## Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

Open the provided local URL in your browser.

### App workflow

1. Upload PDF or TXT documents in the `Upload Documents` tab.
2. Click `Index Documents` to store document embeddings in FAISS.
3. Ask a question in the `Ask Question` tab to retrieve answers from indexed content.
4. Use the `Generate Q&A` tab to create interview questions and answers for a chosen topic.

## Project structure

- `app.py` - Streamlit UI and app flow
- `src/config.py` - project configuration and constants
- `src/document_loader.py` - file upload, document loading, and text splitting
- `src/embedding_service.py` - embedding model initialization
- `src/vector_store.py` - FAISS vector store persistence and search
- `src/llm_service.py` - Groq LLM initialization
- `src/rag_service.py` - retrieval-augmented generation and prompt orchestration
- `src/prompts.py` - prompts for answering questions and generating Q&A

## Notes

- Document chunks are split using a 1000-character window with 150-character overlap.
- The vector store is saved in `data/faiss_db/index.faiss`.
- The app uses `sentence-transformers/all-MiniLM-L6-v2` for embeddings and `llama-3.3-70b-versatile` for generation.

## License

This project does not include a license file. Add a license if you plan to share or publish the repository.
