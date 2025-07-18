from flask import Flask
from app.extensions import db, migrate, jwt, cors
from app.routes import register_routes
from .config import Config
from app.models import User, Teacher, Student
from app.utils.token_blacklist import token_blacklist
from app.utils.token_scheduler import cleanup_scheduler


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化 extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    # 註冊藍圖
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    return app