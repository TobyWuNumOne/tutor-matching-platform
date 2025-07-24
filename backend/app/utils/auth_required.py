"""
檔案: auth_required.py
功能: 建立自定義的JWT身份驗證與授權裝飾器(decorator)。
"""

from functools import wraps
from flask import request, jsonify
import jwt
from app.models.user import User
from app.extensions import db
import os


def auth_required(f):
    """
    認證裝飾器，驗證 JWT token 並將用戶資訊傳遞給路由函數
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # 從 Authorization header 獲取 token
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]  # Bearer <token>
            except IndexError:
                return jsonify({
                    'success': False,
                    'message': 'Token 格式錯誤'
                }), 401
        
        if not token:
            return jsonify({
                'success': False,
                'message': '缺少認證 token'
            }), 401
        
        try:
            # 解碼 JWT token
            secret_key = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
            data = jwt.decode(token, secret_key, algorithms=['HS256'])
            
            # 查找用戶
            current_user = User.query.get(data['user_id'])
            if not current_user:
                return jsonify({
                    'success': False,
                    'message': '用戶不存在'
                }), 401
            
            # 將用戶資訊傳遞給路由函數
            return f(current_user, *args, **kwargs)
            
        except jwt.ExpiredSignatureError:
            return jsonify({
                'success': False,
                'message': 'Token 已過期'
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                'success': False,
                'message': 'Token 無效'
            }), 401
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'認證失敗: {str(e)}'
            }), 401
    
    return decorated_function


def admin_required(f):
    """
    管理員權限裝飾器，需要先通過 auth_required
    """
    @wraps(f)
    @auth_required
    def decorated_function(current_user, *args, **kwargs):
        if not current_user.is_admin:
            return jsonify({
                'success': False,
                'message': '需要管理員權限'
            }), 403
        
        return f(current_user, *args, **kwargs)
    
    return decorated_function


def teacher_required(f):
    """
    老師權限裝飾器，需要先通過 auth_required
    """
    @wraps(f)
    @auth_required
    def decorated_function(current_user, *args, **kwargs):
        if not hasattr(current_user, 'teacher') or not current_user.teacher:
            return jsonify({
                'success': False,
                'message': '需要老師權限'
            }), 403
        
        return f(current_user, *args, **kwargs)
    
    return decorated_function


def student_required(f):
    """
    學生權限裝飾器，需要先通過 auth_required
    """
    @wraps(f)
    @auth_required
    def decorated_function(current_user, *args, **kwargs):
        if not hasattr(current_user, 'student') or not current_user.student:
            return jsonify({
                'success': False,
                'message': '需要學生權限'
            }), 403
        
        return f(current_user, *args, **kwargs)
    
    return decorated_function