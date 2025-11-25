from flask import Blueprint, request, session
from app_server import db
from app_server.model.comment_model import Comment
from app_server.model.post_model import Post

comment_bp = Blueprint("comment_bp", __name__)


@comment_bp.post("/api/comment/<int:post_uuid>")
def add_comment(post_uuid):
    """댓글 작성"""
    user_uuid = session.get("user_uuid")
    if not user_uuid:
        return {"ok": False, "message": "로그인이 필요합니다."}, 401

    data = request.get_json(silent=True) or {}
    content = data.get("content")

    if not content:
        return {"ok": False, "message": "내용이 필요합니다."}, 400

    # 게시글 존재 확인
    post = Post.query.filter_by(post_uuid=post_uuid).first()
    if not post:
        return {"ok": False, "message": "게시글 없음"}, 404

    comment = Comment(
        user_uuid=user_uuid,
        post_uuid=post_uuid,
        comment_content=content,
    )
    db.session.add(comment)
    db.session.commit()

    return {"ok": True, "comment_id": comment.comment_uuid}, 201


@comment_bp.get("/api/comment/<int:post_uuid>")
def get_comments(post_uuid):
    """해당 게시글의 댓글 목록"""
    comments = (
        Comment.query.filter_by(post_uuid=post_uuid)
        .order_by(Comment.create_time.asc())
        .all()
    )

    return {
        "ok": True,
        "comments": [
            {
                "id": c.comment_uuid,
                "user_uuid": c.user_uuid,
                "post_uuid": c.post_uuid,
                "content": c.comment_content,
                "created_at": c.create_time.isoformat()
                if c.create_time
                else "",
            }
            for c in comments
        ],
    }, 200
