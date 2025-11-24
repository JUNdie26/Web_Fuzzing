from flask import Blueprint, jsonify, session
from app_server.model.user_model import User

user_bp = Blueprint("user", __name__)

@user_bp.get("/me")
def get_me():
    # 로그인 안 되어 있으면 None 반환
    uid = session.get("user_id")
    if not uid:
        return {"ok": False, "user": None}, 200

    user = User.query.filter_by(user_id=uid).first()
    if not user:
        return {"ok": False, "user": None}, 200

    return {"ok": True, "user": user.to_dict()}, 200
