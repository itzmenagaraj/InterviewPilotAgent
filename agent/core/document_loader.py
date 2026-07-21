import os

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from core.config import DOCUMENTS_DIR, CHUNK_SIZE, CHUNK_OVERLAP


def save_uploaded_files(uploaded_files):
    from werkzeug.utils import secure_filename

    saved_paths = []

    for uploaded_file in uploaded_files:
        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join(DOCUMENTS_DIR, filename)

        with open(file_path, "wb") as file:
            file.write(uploaded_file.read())

        saved_paths.append(file_path)

    return saved_paths


def load_document(file_path):
    if file_path.lower().endswith(".pdf"):
        return PyPDFLoader(file_path).load()

    if file_path.lower().endswith(".txt"):
        return TextLoader(file_path, encoding="utf-8").load()

    return []


def load_documents(file_paths):
    docs = []

    for file_path in file_paths:
        docs.extend(load_document(file_path))

    return docs


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    return splitter.split_documents(documents)
