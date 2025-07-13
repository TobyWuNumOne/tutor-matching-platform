from flask import Flask
from app.extensions import db, migrate, jwt, cors
from app.routes.auth_routes import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.DevConfig")

    # 初始化 extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    # 註冊藍圖
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    return app