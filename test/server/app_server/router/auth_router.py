# app_server/routes/auth_routes.py
from flask import Blueprint, request, jsonify
from app_server import db
from app_server.model.user_model import User  # 실제 경로 맞게

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    user_id = data.get("user_id")
    password = data.get("password")

    if not user_id or not password:
        return jsonify({"ok": False, "error": "user_id, password are required"}), 400

    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return jsonify({"ok": False, "error": "존재하지 않는 아이디입니다."}), 401

    # 해시 안 쓰면 그냥 평문 비교
    if user.user_password != password:
        return jsonify({"ok": False, "error": "비밀번호가 일치하지 않습니다."}), 401

    return jsonify(
        {
            "ok": True,
            "user": {
                "user_uuid": user.user_uuid,  # PK
                "user_id": user.user_id,
                "user_name": user.user_name,
            },
        }
    )


@auth_bp.route("/logout", methods=["POST"])
def logout():
    # 세션 안 쓰면 그냥 ok만 줘도 됨
    return jsonify({"ok": True})
