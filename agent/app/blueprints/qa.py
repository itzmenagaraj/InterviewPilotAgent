from flask import Blueprint, request, jsonify

from core.rag_service import answer_question, generate_qa

qa_bp = Blueprint("qa", __name__)

_VALID_DIFFICULTIES = {"Beginner", "Intermediate", "Advanced"}


@qa_bp.route("/answer", methods=["POST"])
def answer():
    data = request.get_json(silent=True) or {}
    question = str(data.get("question", "")).strip()

    if not question:
        return jsonify({"error": "question is required"}), 400

    try:
        answer_text, sources = answer_question(question)
        return jsonify({"answer": answer_text, "sources": sources})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@qa_bp.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}
    topic = str(data.get("topic", "")).strip()
    difficulty = str(data.get("difficulty", "Intermediate"))
    raw_count = data.get("count", 5)

    if not topic:
        return jsonify({"error": "topic is required"}), 400

    if difficulty not in _VALID_DIFFICULTIES:
        return jsonify({"error": "difficulty must be Beginner, Intermediate, or Advanced"}), 400

    try:
        count = int(raw_count)
        if not 1 <= count <= 50:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"error": "count must be an integer between 1 and 50"}), 400

    try:
        result, sources = generate_qa(topic, difficulty, count)
        return jsonify({"result": result, "sources": sources})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500
