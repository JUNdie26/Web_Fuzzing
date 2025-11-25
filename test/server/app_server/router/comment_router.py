from flask import Blueprint, request, jsonify
# app_server/service/comment_service.py

from .. import db
from ..model.comment_model import Comment


comment_bp = Blueprint("comment", __name__, url_prefix="/comment")


# 🔹 댓글 생성: 프론트 axios.post("/comment/api/comment_create", {...})
@comment_bp.route("/api/comment_create", methods=["POST"])
def create_comment():
    data = request.get_json()
    post_uuid = data.get("post_uuid")
    content = data.get("content")

    if not post_uuid or not content:
        return jsonify({"error": "post_uuid and content are required"}), 400

    comment = Comment(post_uuid=post_uuid, content=content)
    db.session.add(comment)
    db.session.commit()

    return jsonify(
        {
            "message": "Comment created",
            "comment": {
                "id": comment.comment_uuid,
                "post_uuid": comment.post_uuid,
                "content": comment.content,
                "created_at": comment.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            },
        }
    ), 201


# 🔹 댓글 목록: 프론트 axios.get("/comment/api/comment_list", { params: { post_uuid } })
@comment_bp.route("/api/comment_list", methods=["GET"])
def list_comments():
    post_uuid = request.args.get("post_uuid", type=int)
    if post_uuid is None:
        return jsonify({"error": "post_uuid is required"}), 400

    comments = (
        Comment.query.filter_by(post_uuid=post_uuid)
        .order_by(Comment.create_time.asc())
        .all()
    )

    result = [
        {
            "id": c.comment_uuid,
            "post_uuid": c.post_uuid,
            "content": c.content,
            "created_at": c.create_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        for c in comments
    ]

    return jsonify({"comments": result})


# 🔹 댓글 삭제: 프론트 axios.delete(`/comment/api/comment_delete/${id}`, { params: { post_uuid } })
@comment_bp.route("/api/comment_delete/<int:comment_uuid>", methods=["DELETE"])
def delete_comment(comment_uuid):
    post_uuid = request.args.get("post_uuid", type=int)

    q = Comment.query.filter_by(comment_uuid=comment_uuid)
    if post_uuid is not None:
        q = q.filter_by(post_uuid=post_uuid)

    comment = q.first()
    if not comment:
        return jsonify({"error": "Comment not found"}), 404

    db.session.delete(comment)
    db.session.commit()

    return jsonify({"message": "Comment deleted"})
