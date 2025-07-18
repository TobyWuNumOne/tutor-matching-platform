"""
檔案: auth_required.py
功能: 建立一個自定義的JWT身份驗證裝飾器(decorator)。
"""

from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps


def jwt_required_custom(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        current_user_id = int(get_jwt_identity())  # 轉換為整數

        return f(current_user_id, *args, **kwargs)

    return wrapper
