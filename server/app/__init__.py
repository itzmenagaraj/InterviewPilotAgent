from flask import Flask
from flask_cors import CORS

from app.config import ALLOWED_ORIGINS
from app.blueprints.documents import documents_bp
from app.blueprints.qa import qa_bp


def create_app():
    app = Flask(__name__)
    CORS(app, origins=ALLOWED_ORIGINS)

    app.register_blueprint(documents_bp, url_prefix="/api/documents")
    app.register_blueprint(qa_bp, url_prefix="/api/qa")

    @app.route("/health")
    def health():
        return {"status": "ok"}

    return app
