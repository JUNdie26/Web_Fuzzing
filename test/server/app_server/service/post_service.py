from app_server import db
from app_server.model.post_model import Post
from app_server.model.user_model import User
from datetime import datetime

class PostService:
    @staticmethod
    def create_post(user_id_str, title, content):

        # user_id_str = 세션의 user_id (문자열 아이디)
        user = User.query.filter_by(user_id=user_id_str).first()
        if not user:
            return {"ok": False, "error": "invalid user"}, 400

        post = Post(
            user_id=user.user_uuid,  # PK 사용
            title=title,
            content=content,
            created_at=datetime.utcnow()
        )

        db.session.add(post)
        db.session.commit()

        return {"ok": True, "post_id": post.id}, 201

    @staticmethod
    def get_post(post_id):
        post = Post.query.get(post_id)
        if not post:
            return {"ok": False, "error": "not found"}, 404

        return {
            "ok": True,
            "post": {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "created_at": str(post.created_at)
            }
        }
