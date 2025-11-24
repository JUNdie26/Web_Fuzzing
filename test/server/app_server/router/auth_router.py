from flask import Blueprint, request, jsonify, session
from app_server import db
from ..model.user_model import User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id")
    password = data.get("password")

    if not user_id or not password:
        return jsonify({"ok": False, "error": "required: user_id, password"}), 400

    if User.query.filter_by(user_id=user_id).first():
        return jsonify({"ok": False, "error": "user_id exists"}), 409

    user = User(
        user_id=user_id,
        password=generate_password_hash(password),
        name=user_id
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"ok": True, "user": user.to_dict()}), 201


@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id")
    password = data.get("password")

    if not user_id or not password:
        return jsonify({"ok": False, "error": "required: user_id, password"}), 400

    user = User.query.filter_by(user_id=user_id).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"ok": False, "error": "invalid credentials"}), 401

    session["user_id"] = user.user_id

    return jsonify({"ok": True, "user": user.to_dict()}), 200
