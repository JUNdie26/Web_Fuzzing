# post_app.py
from models import db, Post
from datetime import datetime

class PostService:
    @staticmethod
    def create_post(user_id, title, content):
        
        if not title or not content:
            return {
                "success": False,
                "message": "제목과 내용을 모두 입력해야 합니다."
            }, 400

        new_post = Post(
            user_id = user_id,
            title = title,
            content = content,
            created_at = datetime.now()
        )

        try:
            db.session.add(new_post)
            db.session.commit()
            return {
                "success": True,
                "message": "포스트가 성공적으로 작성되었습니다.",
                "post_id": new_post.id
            }, 201

        except Exception as e:
            db.session.rollback()
            return {
                "success": False,
                "message": f"DB 오류: {str(e)}"
            }, 500

    @staticmethod
    def get_post(post_id):
        """
        포스트 읽기 비즈니스 로직
        """
        post = Post.query.filter_by(id = post_id).first()

        if not post:
            return {
                "success": False,
                "message": "해당 글이 존재하지 않습니다."
            }, 404

        return {
            "success": True,
            "post": {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "user_id": post.user_id,
                "created_at": post.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
        }, 200
