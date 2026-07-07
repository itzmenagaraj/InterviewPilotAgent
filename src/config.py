import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.getcwd()

DOCUMENTS_DIR = os.path.join(BASE_DIR, "data", "documents")
FAISS_DIR = os.path.join(BASE_DIR, "data", "faiss_db")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = "llama-3.3-70b-versatile"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
RETRIEVAL_K = 5

os.makedirs(DOCUMENTS_DIR, exist_ok=True)
os.makedirs(FAISS_DIR, exist_ok=True)