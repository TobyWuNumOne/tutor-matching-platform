from flask import Flask
from flasgger import Swagger
from app.extensions import db, migrate, jwt, cors
from app.routes import register_routes
from .config import Config
from app.models import User, Teacher, Student, Course
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

    # 初始化 Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs/"  # Swagger UI 路徑
    }
    
    swagger = Swagger(app, config=swagger_config)
    


    # 啟動token清理調度器（僅在非測試環境）
    if app.config.get("ENV") != "testing":
        cleanup_scheduler.start()

    # JWT 黑名單檢查
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return token_blacklist.is_token_revoked(jti)

    # JWT錯誤處理
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return {"message": "Token已被撤銷，請重新登入"}, 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        token_type = jwt_payload.get("type", "access")
        return {
            "message": f"{token_type.capitalize()} token已過期",
            "error": "token_expired",
        }, 401

    # 註冊所有路由
    register_routes(app)

    return app
