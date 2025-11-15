from flask import Blueprint, request, session
from app.post_app import PostService

post_bp = Blueprint("post", __name__)

@post_bp.route("/api/post_create", methods=["POST"])
def create_post():
    if "user_id" not in session:
        return {"success": False, "message": "로그인이 필요합니다."}, 401

    data = request.json
    return PostService.create_post(
        user_id=session["user_id"],
        title=data.get("title"),
        content=data.get("content")
    )

@post_bp.route("/api/post/<int:post_id>", methods=["GET"])
def read_post(post_id):
    return PostService.get_post(post_id)

