from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models.user import User
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    user = User(username=data["username"], password=generate_password_hash(data["password"]))
    db.session.add(user)
    db.session.commit()
    return jsonify(msg="註冊成功"), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()
    if user and check_password_hash(user.password, data["password"]):
        token = create_access_token(identity=user.username)
        return jsonify(access_token=token), 200
    return jsonify(msg="登入失敗"), 401
