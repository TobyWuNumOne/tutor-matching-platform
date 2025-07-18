"""
檔案: jwt_handler.py
功能: 建立JWT Token，並將使用者ID嵌入在Token中，
"""

from flask_jwt_extended import create_access_token


def generate_token(user_id):
    return create_access_token(identity=user_id)
