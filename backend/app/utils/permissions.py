"""
權限驗證裝飾器
"""

from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from app.models.user import User


def admin_required(f):
    """
    檢查當前用戶是否為管理員的裝飾器
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 驗證JWT token
        verify_jwt_in_request()

        # 取得當前用戶ID
        current_user_id = get_jwt_identity()

        # 查詢用戶資料 (將字符串ID轉換為整數)
        user = User.query.get(int(current_user_id))

        if not user:
            return jsonify({"error": "用戶不存在"}), 401

        if user.role != "admin":
            return jsonify({"error": "權限不足，僅管理員可執行此操作"}), 403

        return f(*args, **kwargs)

    return decorated_function


def role_required(*allowed_roles):
    """
    檢查用戶角色的裝飾器

    Args:
        allowed_roles: 允許的角色列表
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 驗證JWT token
            verify_jwt_in_request()

            # 取得當前用戶ID
            current_user_id = get_jwt_identity()

            # 查詢用戶資料 (將字符串ID轉換為整數)
            user = User.query.get(int(current_user_id))

            if not user:
                return jsonify({"error": "用戶不存在"}), 401

            if user.role not in allowed_roles:
                return (
                    jsonify(
                        {
                            "error": f"權限不足，僅 {', '.join(allowed_roles)} 可執行此操作"
                        }
                    ),
                    403,
                )

            return f(*args, **kwargs)

        return decorated_function

    return decorator
