from flask import Blueprint, request, jsonify, session
from .. import db
from ..model.user_model import User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

# 회원가입
@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    user_id = (data.get("user_id") or "").strip()
    password = (data.get("password") or "").strip()
    name = (data.get("name") or "").strip()

    if not user_id or not password or not name:
        return jsonify({"ok": False, "error": "required: user_id, password, name"}), 400

    # 중복 체크
    if User.query.filter_by(user_id=user_id).first():   
        return jsonify({"ok": False, "error": "user_id exists"}), 409

    user = User(user_id=user_id,
                password=generate_password_hash(password),
                name=name)
    db.session.add(user)
    db.session.commit()

    return jsonify({"ok": True, "user": user.to_dict()}), 201


# 로그인
@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    user_id = (data.get("user_id") or "").strip()
    password = (data.get("password") or "").strip()

    if not user_id or not password:
        return jsonify({"ok": False, "error": "required: user_id, password"}), 400

    user = User.query.filter_by(user_id=user_id).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"ok": False, "error": "invalid credentials"}), 401

    # 세션에 user_id만 보관
    session["user_id"] = user.user_id
    return jsonify({"ok": True, "user": user.to_dict()}), 200


# 로그아웃
@auth_bp.post("/logout")
def logout():
    session.pop("user_id", None)
    return jsonify({"ok": True}), 200


# 세션 확인
@auth_bp.get("/me")
def me():
    uid = session.get("user_id")
    if not uid:
        return jsonify({"ok": False, "user": None}), 200
    user = User.query.filter_by(user_id=uid).first()
    return jsonify({"ok": True, "user": user.to_dict() if user else None}), 200
