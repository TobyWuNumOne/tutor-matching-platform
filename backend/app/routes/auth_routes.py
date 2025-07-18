from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models.user import User
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from app.schemas import UserCreateSchema, UserResponseSchema
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


