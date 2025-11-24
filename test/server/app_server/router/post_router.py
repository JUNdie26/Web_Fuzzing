from flask import Blueprint, request, jsonify, session
from app_server.service.post_service import PostService

post_bp = Blueprint("post_bp", __name__)

@post_bp.post("/api/post_create")
def create_post():
    if "user_id" not in session:
        return {"ok": False, "message": "로그인이 필요합니다."}, 401

    data = request.json
    return PostService.create_post(
        user_id_str=session["user_id"],
        title=data.get("title"),
        content=data.get("content")
    )
