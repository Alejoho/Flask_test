from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "secret"
    app.config["HUNTER_API_KEY"] = os.getenv("HUNTER_API_KEY")

    from app.routes import index_routes_bp

    app.register_blueprint(index_routes_bp)

    return app
