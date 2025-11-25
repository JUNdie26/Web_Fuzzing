# app_server/routes/post_routes.py

from flask import Blueprint, request, jsonify, current_app
from sqlalchemy.exc import IntegrityError, DataError
from app_server import db
from app_server.model.post_model import Post

post_bp = Blueprint("post", __name__, url_prefix="/post")


# 🔹 게시글 목록
@post_bp.route("/api/posts", methods=["GET"])
@post_bp.route("/api/all", methods=["GET"])
def get_posts():
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "", type=str)

    query = Post.query
    if search:
        query = query.filter(Post.post_title.like(f"%{search}%"))

    pagination = query.order_by(Post.create_time.desc()).paginate(
        page=page, per_page=10, error_out=False
    )

    posts = [
        {
            "id": p.post_uuid,
            "title": p.post_title,
            "content": p.post_content,
            "created_at": p.create_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for p in pagination.items
    ]

    return jsonify(
        {
            "posts": posts,
            "page": pagination.page,
            "pages": pagination.pages,
            "total": pagination.total,
        }
    )


# 🔹 게시글 생성
@post_bp.route("/api/post_create", methods=["POST"])
def create_post():
    """
    프론트에서 오는 JSON:
    {
      "title": "...",
      "content": "...",
      "user_uuid": <user.user_uuid 정수>   // 여기 중요
    }
    """
    try:
        data = request.get_json() or {}
        current_app.logger.info(f"post_create payload = {data}")

        title = data.get("title")
        content = data.get("content")
        # user_uuid 또는 user_id 어느 쪽이 와도 받아준다.
        user_uuid = data.get("user_uuid") or data.get("user_id")

        if not title or not content or not user_uuid:
            return jsonify({"error": "title, content, user_uuid are required"}), 400

        try:
            user_uuid = int(user_uuid)
        except (TypeError, ValueError):
            return jsonify({"error": "user_uuid must be an integer"}), 400

        post = Post(
            post_title=title,
            post_content=content,
            user_uuid=user_uuid,
        )
        db.session.add(post)
        db.session.commit()

        return jsonify({"message": "Post created", "post_id": post.post_uuid}), 201

    except (IntegrityError, DataError) as e:
        db.session.rollback()
        current_app.logger.exception("post_create DB error")
        return (
            jsonify(
                {
                    "error": "DB constraint error",
                    "detail": str(e.orig) if hasattr(e, "orig") else str(e),
                }
            ),
            400,
        )

    except Exception as e:
        db.session.rollback()
        current_app.logger.exception("post_create unknown error")
        return jsonify({"error": "internal server error", "detail": str(e)}), 500


# 🔹 게시글 상세
@post_bp.route("/api/post/<int:post_uuid>", methods=["GET"])
@post_bp.route("/<int:post_uuid>", methods=["GET"])
def get_post(post_uuid):
    post = Post.query.get_or_404(post_uuid)

    return jsonify(
        {
            "id": post.post_uuid,
            "title": post.post_title,
            "content": post.post_content,
            "created_at": post.create_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
    )


# 🔹 게시글 수정
@post_bp.route("/api/post_update/<int:post_uuid>", methods=["PUT"])
def update_post(post_uuid):
    data = request.get_json() or {}
    title = data.get("title")
    content = data.get("content")

    post = Post.query.get_or_404(post_uuid)

    if title:
        post.post_title = title
    if content:
        post.post_content = content

    db.session.commit()
    return jsonify({"message": "Post updated"})


# 🔹 게시글 삭제
@post_bp.route("/api/post_delete", methods=["POST"])
def delete_post():
    data = request.get_json() or {}
    post_uuid = data.get("post_uuid")

    if not post_uuid:
        return jsonify({"error": "post_uuid is required"}), 400

    post = Post.query.get_or_404(post_uuid)
    db.session.delete(post)
    db.session.commit()

    return jsonify({"message": "Post deleted"})
