import os
from flask import Flask, render_template, session
from flask_session import Session
from db import init_db, db
from api import api_bp

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")

    # Secret key and session config
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-change-me")
    # Server-side filesystem sessions to persist a session_id used for style/dataset ownership
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SESSION_FILE_DIR"] = os.path.join(os.path.dirname(__file__), ".flask_sessions")
    os.makedirs(app.config["SESSION_FILE_DIR"], exist_ok=True)
    Session(app)

    # Database configuration
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///plasmidflow.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize DB
    init_db(app)

    # Blueprints
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.route("/")
    def index():
        # Ensure session is initialized
        if "sid" not in session:
            import uuid
            session["sid"] = str(uuid.uuid4())
        return render_template("index.html")

    @app.route("/health")
    def health():
        return {"status": "ok"}

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", "10000"))
    host = os.getenv("HOST", "0.0.0.0")
    debug = os.getenv("FLASK_DEBUG", "1") == "1"
    print(f"PlasmidFlow (Flask) running on {host}:{port}")
    app.run(host=host, port=port, debug=debug)