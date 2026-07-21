import requests
from flask import Blueprint, request, jsonify

from app.config import AGENT_BASE_URL

qa_bp = Blueprint("qa", __name__)


@qa_bp.route("/answer", methods=["POST"])
def answer():
    try:
        resp = requests.post(
            f"{AGENT_BASE_URL}/api/qa/answer",
            json=request.get_json(silent=True) or {},
            timeout=60,
        )
        return jsonify(resp.json()), resp.status_code
    except requests.RequestException:
        return jsonify({"error": "Agent service is unavailable"}), 502


@qa_bp.route("/generate", methods=["POST"])
def generate():
    try:
        resp = requests.post(
            f"{AGENT_BASE_URL}/api/qa/generate",
            json=request.get_json(silent=True) or {},
            timeout=120,
        )
        return jsonify(resp.json()), resp.status_code
    except requests.RequestException:
        return jsonify({"error": "Agent service is unavailable"}), 502
