# 登入、註冊（JWT）
from flask import Blueprint, request, jsonify
from app.models.user import User
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from app.schemas import UserCreateSchema, UserResponseSchema
from app.utils.token_blacklist import token_blacklist
from marshmallow import ValidationError

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        schema = UserCreateSchema()
        data = schema.load(request.json)

        # 檢查用戶是否已存在
        if User.query.filter_by(account=data["account"]).first():
            return jsonify({"error": "帳號已註冊過..."}), 400

        # 創建新用戶
        user = User(name=data["name"], account=data["account"], role=data["role"])
        user.set_password(data["password"])
        user.save()

        return jsonify({"message": "帳號註冊成功"}), 201

    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.json
        user = User.query.filter_by(account=data.get("account")).first()

        if user and user.check_password(data.get("password")):
            # 創建 access token 和 refresh token
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))

            return (
                jsonify(
                    {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "user": UserResponseSchema().dump(user),
                        "token_type": "Bearer",
                        "expires_in": 3600,  # 1小時 = 3600秒
                    }
                ),
                200,
            )

        return jsonify({"error": "Invalid credentials"}), 401

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """使用 refresh token 獲取新的 access token"""
    try:
        # 從 refresh token 獲取用戶ID
        current_user_id = get_jwt_identity()

        # 查詢用戶是否存在
        user = User.query.get(int(current_user_id))
        if not user:
            return jsonify({"error": "用戶不存在"}), 401

        # 創建新的 access token
        new_access_token = create_access_token(identity=str(user.id))

        return (
            jsonify(
                {
                    "access_token": new_access_token,
                    "token_type": "Bearer",
                    "expires_in": 3600,  # 1小時 = 3600秒
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """登出 - 將當前access token加入黑名單"""
    try:
        jwt_data = get_jwt()
        jti = jwt_data["jti"]  # JWT ID
        exp = jwt_data["exp"]  # 過期時間

        # 添加到黑名單，標記為access token
        token_blacklist.add_token(jti, exp, "access")
        return jsonify({"message": "成功登出"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/logout-refresh", methods=["POST"])
@jwt_required(refresh=True)
def logout_refresh():
    """登出 refresh token - 將 refresh token 加入黑名單"""
    try:
        jwt_data = get_jwt()
        jti = jwt_data["jti"]  # JWT ID
        exp = jwt_data["exp"]  # 過期時間

        # 添加到黑名單，標記為refresh token
        token_blacklist.add_token(jti, exp, "refresh")
        return jsonify({"message": "Refresh token 已撤銷"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/logout-all", methods=["POST"])
@jwt_required()
def logout_all():
    """登出所有token - 將access token和對應的refresh token都加入黑名單"""
    try:
        jwt_data = get_jwt()
        jti = jwt_data["jti"]
        exp = jwt_data["exp"]

        # 添加當前access token到黑名單
        token_blacklist.add_token(jti, exp, "access")

        # 注意：這裡我們只能撤銷當前的access token
        # 要撤銷對應的refresh token，需要額外的邏輯來追蹤token關係

        return jsonify({"message": "成功登出當前token"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route("/token-status", methods=["GET"])
@jwt_required()
def token_status():
    """檢查黑名單狀態（僅管理員可用）"""
    try:
        # 檢查是否為管理員
        current_user_id = get_jwt_identity()
        user = User.query.get(int(current_user_id))

        if not user or user.role != "admin":
            return jsonify({"error": "權限不足"}), 403

        # 清理過期token並獲取統計信息
        cleaned_count = token_blacklist.cleanup_expired_tokens()
        stats = token_blacklist.get_blacklist_stats()

        return (
            jsonify(
                {
                    "blacklist_stats": stats,
                    "cleaned_expired_tokens": cleaned_count,
                    "message": "黑名單狀態更新完成",
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
