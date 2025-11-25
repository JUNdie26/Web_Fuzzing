from flask import Blueprint, request, session
from app_server.service.post_service import PostService

post_bp = Blueprint("post_bp", __name__)


@post_bp.post("/api/post_create")
def create_post():
    user_uuid = session.get("user_uuid")
    if not user_uuid:
        return {"ok": False, "message": "로그인이 필요합니다."}, 401

    data = request.get_json(silent=True) or {}
    title = data.get("title")
    content = data.get("content")

    return PostService.create_post(
        user_uuid=user_uuid,
        title=title,
        content=content,
    )


@post_bp.get("/api/all")
def get_all_posts():
    return PostService.get_all_posts()


@post_bp.get("/api/post/<int:post_id>")
def get_post(post_id: int):
    return PostService.get_post(post_id)
