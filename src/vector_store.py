import os

from langchain_community.vectorstores import FAISS

from src.config import FAISS_DIR, RETRIEVAL_K
from src.embedding_service import get_embeddings

embeddings = get_embeddings()


def load_vector_store():
    index_path = os.path.join(FAISS_DIR, "index.faiss")

    if os.path.exists(index_path):
        return FAISS.load_local(
            FAISS_DIR,
            embeddings,
            allow_dangerous_deserialization=True
        )

    return None


def save_vector_store(vector_store):
    vector_store.save_local(FAISS_DIR)


def add_documents_to_vector_store(chunks):
    vector_store = load_vector_store()

    if vector_store is None:
        vector_store = FAISS.from_documents(chunks, embeddings)
    else:
        vector_store.add_documents(chunks)

    save_vector_store(vector_store)

    return len(chunks)


def search_documents(query):
    vector_store = load_vector_store()

    if vector_store is None:
        return []

    return vector_store.similarity_search(query, k=RETRIEVAL_K)