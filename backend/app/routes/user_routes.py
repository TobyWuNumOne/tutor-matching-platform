from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.schemas.user_schema import UserResponseSchema
from app.utils.auth_required import admin_required
from flasgger.utils import swag_from

user_bp = Blueprint("user", __name__)


# Get all users (admin only)
@user_bp.route("", methods=["GET"])
@swag_from({
    'tags': ['用戶'],
    'summary': '取得所有用戶（僅限管理員）',
    'responses': {
        200: {
            'description': '用戶列表',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer', 'example': 1},
                        'name': {'type': 'string', 'example': '王小明'},
                        'account': {'type': 'string', 'example': 'user123'},
                        'role': {'type': 'string', 'example': 'student'},
                        'created_at': {'type': 'string', 'example': '2024-07-31T10:00:00'},
                        'updated_at': {'type': 'string', 'example': '2024-07-31T10:00:00'}
                    }
                }
            }
        }
    }
})
@jwt_required()
@admin_required
def get_all_users():
    users = User.query.all()
    schema = UserResponseSchema(many=True)
    return jsonify(schema.dump(users)), 200


# Get user by ID
@user_bp.route("/<int:user_id>", methods=["GET"])
@swag_from({
    'tags': ['用戶'],
    'summary': '依ID取得用戶',
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': '用戶ID'
        }
    ],
    'responses': {
        200: {
            'description': '用戶資料',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer', 'example': 1},
                    'name': {'type': 'string', 'example': '王小明'},
                    'account': {'type': 'string', 'example': 'user123'},
                    'role': {'type': 'string', 'example': 'student'},
                    'created_at': {'type': 'string', 'example': '2024-07-31T10:00:00'},
                    'updated_at': {'type': 'string', 'example': '2024-07-31T10:00:00'}
                }
            }
        },
        403: {'description': '權限不足'},
        404: {'description': '找不到用戶'}
    }
})
@jwt_required()
def get_user(user_id):
    # Get current user's ID from token
    current_user_id = get_jwt_identity()

    # If not admin, only allow access to own profile
    if str(current_user_id) != str(user_id):
        user = User.query.filter_by(id=current_user_id).first()
        if not user or user.role != "admin":
            return jsonify({"message": "Access denied"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    schema = UserResponseSchema()
    return jsonify(schema.dump(user)), 200


# Update user by ID (only own account or admin)
@user_bp.route("/<int:user_id>", methods=["PUT"])
@swag_from({
    'tags': ['用戶'],
    'summary': '更新用戶資料',
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': '用戶ID'
        },
        {
            'name': 'body',
            'in': 'body',
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string', 'example': '王小明'},
                    'account': {'type': 'string', 'example': 'user123'},
                    'password': {'type': 'string', 'example': '12345678'},
                    'role': {'type': 'string', 'enum': ['teacher', 'student', 'admin'], 'example': 'student'}
                }
            },
            'required': True,
            'description': '要更新的欄位'
        }
    ],
    'responses': {
        200: {
            'description': '更新後的用戶資料',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer', 'example': 1},
                    'name': {'type': 'string', 'example': '王小明'},
                    'account': {'type': 'string', 'example': 'user123'},
                    'role': {'type': 'string', 'example': 'student'},
                    'created_at': {'type': 'string', 'example': '2024-07-31T10:00:00'},
                    'updated_at': {'type': 'string', 'example': '2024-07-31T10:00:00'}
                }
            }
        },
        403: {'description': '權限不足'},
        404: {'description': '找不到用戶'}
    }
})
@jwt_required()
def update_user(user_id):
    # Get current user's ID from token
    current_user_id = get_jwt_identity()

    # If not admin, only allow access to own profile
    if str(current_user_id) != str(user_id):
        user = User.query.filter_by(id=current_user_id).first()
        if not user or user.role != "admin":
            return jsonify({"message": "Access denied"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()

    # Don't allow role changes from non-admin users
    if "role" in data and str(current_user_id) != str(user_id):
        current_user = User.query.filter_by(id=current_user_id).first()
        if not current_user or current_user.role != "admin":
            data.pop("role")

    # Don't allow password updates through this endpoint for security
    if "password" in data:
        data.pop("password")

    # Update allowed fields
    for key, value in data.items():
        if hasattr(user, key):
            setattr(user, key, value)

    user.save()

    schema = UserResponseSchema()
    return jsonify(schema.dump(user)), 200


# Delete user (admin only)
@user_bp.route("/<int:user_id>", methods=["DELETE"])
@swag_from({
    'tags': ['用戶'],
    'summary': '刪除用戶（僅限管理員）',
    'parameters': [
        {
            'name': 'user_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': '用戶ID'
        }
    ],
    'responses': {
        200: {'description': '刪除成功'},
        404: {'description': '找不到用戶'}
    }
})
@jwt_required()
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    user.delete()
    return jsonify({"message": "User deleted successfully"}), 200
