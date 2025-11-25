from flask import Blueprint, request, jsonify
from .. import db
from app_server.model.post_model import Post

post_bp = Blueprint("post", __name__, url_prefix="/post")


# 🔹 게시글 목록: 프론트가 /post/api/all 로 요청하니까 거기에 맞춰줌
@post_bp.route("/api/posts", methods=["GET"])
@post_bp.route("/api/all", methods=["GET"])  # 프론트용 alias
def get_posts():
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "", type=str)

    query = Post.query
    if search:
        query = query.filter(Post.title.like(f"%{search}%"))

    pagination = query.order_by(Post.create_time.desc()).paginate(
        page=page, per_page=10, error_out=False
    )

    posts = [
        {
            "id": p.post_uuid,
            "title": p.title,
            "content": p.content,
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


# 🔹 게시글 생성: 프론트 axios.post("/post/api/post_create", ...) 과 이미 맞음
@post_bp.route("/api/post_create", methods=["POST"])
def create_post():
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")
    user_id = data.get("user_id")

    if not title or not content or not user_id:
        return jsonify({"error": "title, content, user_id are required"}), 400

    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()

    return jsonify({"message": "Post created", "post_id": post.post_uuid}), 201


# 🔹 게시글 상세: 프론트가 /post/${id} 로 요청하니까 그 경로도 열어줌
@post_bp.route("/api/post/<int:post_uuid>", methods=["GET"])
@post_bp.route("/<int:post_uuid>", methods=["GET"])  # 프론트용 alias
def get_post(post_uuid):
    post = Post.query.get_or_404(post_uuid)

    return jsonify(
        {
            "id": post.post_uuid,
            "title": post.title,
            "content": post.content,
            "created_at": post.create_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
    )


# 🔹 게시글 수정 (프론트에서 아직 안 쓰지만 그대로 둠)
@post_bp.route("/api/post_update/<int:post_uuid>", methods=["PUT"])
def update_post(post_uuid):
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")

    post = Post.query.get_or_404(post_uuid)

    if title:
        post.title = title
    if content:
        post.content = content

    db.session.commit()
    return jsonify({"message": "Post updated"})


# 🔹 게시글 삭제: 프론트 axios.post("/post/api/post_delete", { post_uuid })
@post_bp.route("/api/post_delete", methods=["POST"])
def delete_post():
    data = request.get_json()
    post_uuid = data.get("post_uuid")

    if not post_uuid:
        return jsonify({"error": "post_uuid is required"}), 400

    post = Post.query.get_or_404(post_uuid)
    db.session.delete(post)
    db.session.commit()

    return jsonify({"message": "Post deleted"})
