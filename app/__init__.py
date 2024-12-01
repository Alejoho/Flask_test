from flask import Flask
from itsdangerous import URLSafeTimedSerializer
from dotenv import load_dotenv
import os

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "secret"
    app.config["HUNTER_API_KEY"] = os.getenv("HUNTER_API_KEY")
    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USERNAME"] = os.getenv("GMAIL_ACCOUNT")
    app.config["MAIL_PASSWORD"] = os.getenv("GMAIL_PASSWORD")
    app.config["MAIL_USE_TLS"] = True

    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    app.config["SERIALIZER"] = serializer

    from app.routes import index_routes_bp

    app.register_blueprint(index_routes_bp)

    return app
