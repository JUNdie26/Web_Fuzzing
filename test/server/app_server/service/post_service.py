from datetime import datetime

from app_server import db
from app_server.model.post_model import Post
from app_server.model.user_model import User


class PostService:
    @staticmethod
    def create_post(user_uuid: int, title: str, content: str):
        if not user_uuid:
            return {"ok": False, "error": "user_uuid is required"}, 400
        if not title or not content:
            return {"ok": False, "error": "title and content are required"}, 400

        user = User.query.filter_by(user_uuid=user_uuid).first()
        if not user:
            return {"ok": False, "error": "invalid user"}, 400

        post = Post(
            user_uuid=user.user_uuid,
            post_title=title,
            post_content=content,
            create_time=datetime.utcnow(),
        )
        db.session.add(post)
        db.session.commit()

        return {"ok": True, "post_id": post.post_uuid}, 201

    @staticmethod
    def get_all_posts():
        posts = Post.query.order_by(Post.create_time.desc()).all()

        # 프론트에서 기대하는 키에 맞게 매핑
        return {
            "ok": True,
            "posts": [
                {
                    "id": p.post_uuid,
                    "title": p.post_title,
                    "content": p.post_content,
                    "created_at": p.create_time.isoformat()
                    if p.create_time
                    else "",
                }
                for p in posts
            ],
        }, 200

    @staticmethod
    def get_post(post_id: int):
        post = Post.query.filter_by(post_uuid=post_id).first()
        if not post:
            return {"ok": False, "error": "not found"}, 404

        return {
            "ok": True,
            "post": {
                "id": post.post_uuid,
                "title": post.post_title,
                "content": post.post_content,
                "created_at": post.create_time.isoformat()
                if post.create_time
                else "",
            },
        }, 200
