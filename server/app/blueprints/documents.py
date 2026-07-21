import requests
from flask import Blueprint, request, jsonify

from app.config import AGENT_BASE_URL

documents_bp = Blueprint("documents", __name__)


@documents_bp.route("/upload", methods=["POST"])
def upload():
    files = request.files.getlist("files")

    if not files or all(f.filename == "" for f in files):
        return jsonify({"error": "No files provided"}), 400

    upload_files = [("files", (f.filename, f.stream, f.mimetype)) for f in files]

    try:
        resp = requests.post(
            f"{AGENT_BASE_URL}/api/documents/upload",
            files=upload_files,
            timeout=120,
        )
        return jsonify(resp.json()), resp.status_code
    except requests.RequestException:
        return jsonify({"error": "Agent service is unavailable"}), 502
