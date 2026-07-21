from flask import Blueprint, request, jsonify

from core.document_loader import load_documents, save_uploaded_files, split_documents
from core.vector_store import add_documents_to_vector_store

documents_bp = Blueprint("documents", __name__)

_ALLOWED_EXTENSIONS = {"pdf", "txt"}


def _allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in _ALLOWED_EXTENSIONS


@documents_bp.route("/upload", methods=["POST"])
def upload():
    files = request.files.getlist("files")

    if not files or all(f.filename == "" for f in files):
        return jsonify({"error": "No files provided"}), 400

    valid_files = [f for f in files if _allowed_file(f.filename)]

    if not valid_files:
        return jsonify({"error": "Only PDF and TXT files are accepted"}), 400

    try:
        file_paths = save_uploaded_files(valid_files)
        documents = load_documents(file_paths)
        chunks = split_documents(documents)
        count = add_documents_to_vector_store(chunks)
        return jsonify({"success": True, "chunks_indexed": count})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500
