from flask import Blueprint, request, jsonify, session
from models import db, Post

post_bp = Blueprint('post_bp', __name__, url_prefix='/api')

# 세션 체크
def require_login():
    if 'user_id' not in session:
        return jsonify({"success": False, "message": "로그인이 필요합니다."}), 401
    return None


# 포스트 작성
@post_bp.route('/post_create', methods=['POST'])
def create_post():
    # 로그인 체크
    check = require_login()
    if check:
        return check

    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    user_id = session['user_id']

    if not title or not content:
        return jsonify({"success": False, "message": "제목과 내용은 필수입니다."}), 400

    new_post = Post(title=title, content=content, author_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    return jsonify({
        "success": True,
        "post_id": new_post.id,
        "message": "포스트 작성 완료"
    }), 201


# 포스트 읽기
@post_bp.route('/post/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get(post_id)

    if not post:
        return jsonify({"success": False, "message": "게시글을 찾을 수 없습니다."}), 404

    return jsonify({
        "success": True,
        "post": {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author_id": post.author_id,
            "created_at": post.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
    }), 200
