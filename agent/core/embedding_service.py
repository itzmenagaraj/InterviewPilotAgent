from langchain_community.embeddings import FastEmbedEmbeddings
from core.config import EMBEDDING_MODEL


def get_embeddings():
    return FastEmbedEmbeddings(
        model_name=EMBEDDING_MODEL
    )
