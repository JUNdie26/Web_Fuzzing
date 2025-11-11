from flask import Blueprint

comment_bp = Blueprint("comment", __name__)

# 프론트에서 서버로 데이터를 넘겨주는 것을 일단 JSON으로 넘겨준다고 가정
# { user_uuid = ..., post_uuid = ..., comment_content = ... }
@comment_bp.route('/api/post/<post_uuid>/comment', methods=['POST'])
def post_comment(post_uuid):
    