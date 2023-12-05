import jwt
from flask import Flask, g
from flask_pymongo import PyMongo
from flask import current_app
from flask_cors import CORS
from datetime import datetime, timedelta


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_pyfile("../settings.py")

    from routes import bp

    app.register_blueprint(bp)

    return app


def get_db():
    if "db" not in g:
        g.db = PyMongo(current_app).db
    return g.db


def encode_auth_token(user_id):
    try:
        payload = {
            "exp": datetime.utcnow() + timedelta(days=1),
            "iat": datetime.utcnow(),
            "sub": user_id,
        }
        return jwt.encode(
            payload, current_app.config.get("SECRET_KEY"), algorithm="HS256"
        )
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(
            auth_token, current_app.config.get("SECRET_KEY"), algorithms="HS256"
        )
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        return "Signature expired. Please log in again."
    except jwt.InvalidTokenError:
        return "Invalid token. Please log in again."
