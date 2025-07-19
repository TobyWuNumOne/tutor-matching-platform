"""
檔案: auth_required.py
功能: 建立自定義的JWT身份驗證與授權裝飾器(decorator)。
"""

from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps
from flask import jsonify
from app.models.user import User


def jwt_required_custom(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user_id = int(get_jwt_identity())  # 轉換為整數

        return f(current_user_id, *args, **kwargs)

    return wrapper


def admin_required(f):
    """
    驗證當前用戶是否為管理員的裝飾器
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user_id = get_jwt_identity()

        # 檢查用戶是否為管理員
        user = User.query.filter_by(id=current_user_id).first()

        if not user or user.role != "admin":
            return jsonify({"message": "管理員權限需要"}), 403

        return f(*args, **kwargs)

    return wrapper


def role_required(allowed_roles):
    """
    驗證當前用戶是否擁有特定角色的裝飾器
    允許傳入單一角色字符串或角色列表
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()

            # 檢查用戶角色
            user = User.query.filter_by(id=current_user_id).first()

            if not user:
                return jsonify({"message": "無效用戶"}), 401

            # 轉換單一角色為列表
            roles = (
                allowed_roles if isinstance(allowed_roles, list) else [allowed_roles]
            )

            if user.role not in roles:
                return jsonify({"message": "權限不足"}), 403

            return f(*args, **kwargs)

        return wrapper

    return decorator
