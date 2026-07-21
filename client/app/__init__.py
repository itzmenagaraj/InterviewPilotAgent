from pathlib import Path

from flask import Flask

from app.blueprints.pages import pages_bp

CLIENT_ROOT = Path(__file__).resolve().parent.parent


def create_app():
    app = Flask(
        __name__,
        template_folder=str(CLIENT_ROOT / "templates"),
        static_folder=str(CLIENT_ROOT / "static"),
    )
    app.register_blueprint(pages_bp)
    return app
