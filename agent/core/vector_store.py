import os

from langchain_community.vectorstores import FAISS

from core.config import FAISS_DIR, RETRIEVAL_K
from core.embedding_service import get_embeddings

_embeddings = None
_vector_store = None


def _get_embeddings():
    global _embeddings
    if _embeddings is None:
        _embeddings = get_embeddings()
    return _embeddings


def load_vector_store():
    global _vector_store

    if _vector_store is not None:
        return _vector_store

    index_path = os.path.join(FAISS_DIR, "index.faiss")

    if os.path.exists(index_path):
        _vector_store = FAISS.load_local(
            FAISS_DIR,
            _get_embeddings(),
            allow_dangerous_deserialization=True
        )

    return _vector_store


def save_vector_store(vector_store):
    global _vector_store
    vector_store.save_local(FAISS_DIR)
    _vector_store = vector_store


def add_documents_to_vector_store(chunks):
    vector_store = load_vector_store()

    if vector_store is None:
        vector_store = FAISS.from_documents(chunks, _get_embeddings())
    else:
        vector_store.add_documents(chunks)

    save_vector_store(vector_store)

    return len(chunks)


def search_documents(query):
    vector_store = load_vector_store()

    if vector_store is None:
        return []

    return vector_store.similarity_search(query, k=RETRIEVAL_K)
