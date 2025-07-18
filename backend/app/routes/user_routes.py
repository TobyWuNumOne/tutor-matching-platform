from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.user import User
from app.schemas.user_schema import UserResponseSchema
from app.utils.auth_required import admin_required

user_bp = Blueprint("user", __name__)


# Get all users (admin only)
@user_bp.route("", methods=["GET"])
@jwt_required()
@admin_required
def get_all_users():
    users = User.query.all()
    schema = UserResponseSchema(many=True)
    return jsonify(schema.dump(users)), 200


# Get user by ID
@user_bp.route("/<int:user_id>", methods=["GET"])
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
@jwt_required()
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    user.delete()
    return jsonify({"message": "User deleted successfully"}), 200
