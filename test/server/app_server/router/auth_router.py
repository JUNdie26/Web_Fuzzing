from flask import Blueprint, request, jsonify, session

from app_server import db
from app_server.model.user_model import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}

    user_id = data.get("user_id")
    password = data.get("password")
    # 프론트에서 이름 안 보내면 일단 아이디랑 동일하게 저장
    user_name = data.get("user_name") or user_id

    if not user_id or not password:
        return jsonify({"ok": False, "error": "required: user_id, password"}), 400

    # 아이디 중복 체크
    if User.query.filter_by(user_id=user_id).first():
        return jsonify({"ok": False, "error": "user_id exists"}), 409

    # 비밀번호는 지금은 해시 X, 그대로 저장 (VARCHAR(45) 한계 때문)
    user = User(
        user_id=user_id,
        user_password=password,
        user_name=user_name,
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

    # 해시 안 쓰니까 그냥 문자열 비교
    if not user or user.user_password != password:
        return jsonify({"ok": False, "error": "invalid credentials"}), 401

    # 세션에 uuid + id 둘 다 넣어두면 나중에 편함
    session["user_uuid"] = user.user_uuid
    session["user_id"] = user.user_id

    return jsonify({"ok": True, "user": user.to_dict()}), 200


@auth_bp.post("/logout")
def logout():
    session.clear()
    return jsonify({"ok": True}), 200
