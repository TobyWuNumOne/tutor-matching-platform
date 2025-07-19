from flask import Flask
from app.extensions import db, migrate, jwt, cors

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.DevConfig")

    # 初始化 extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    # 這裡才導入 models（避免循環導入）
    from app.models import user, teachers, courses
    
    # 註冊藍圖
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    return app