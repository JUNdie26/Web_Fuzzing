from flask import Blueprint, request, jsonify, session
from ..model import comment_model

comment_bp = Blueprint("comment", __name__)

# 프론트에서 서버로 데이터를 넘겨주는 것을 일단 JSON으로 넘겨준다고 가정
# API 엔드포인트는 변경하는게 좋아보임 -> /api/comment
# { post_uuid = ..., comment_content = ... }
@comment_bp.route('/', methods=['POST'])
def post_comment():
    request_json = request.get_json()
    post_uuid = request_json['post_uuid']
    comment_content = request_json['comment_content']

    # 현재 로그인한 상태가 아닌 경우
    # 세션은 user 테이블의 user_id 값이라고 가정함
    if 'user_id' not in session:
        return {'result': 'FAILED'}, 401

    comment_model.add_comment(session['user_id'], post_uuid, comment_content)
    return {'result': 'SUCCESS'}, 200


# 댓글 불러오기, 별도의 인증과정은 필요 없음
# GET 요청은 BODY를 포함하지 않는 것이 REST 표준...
# 따라서 쿼리 파라미터 형식을 채용, /api/comment?post_uuid=3
@comment_bp.route('/', methods=['GET'])
def get_comment():
    post_uuid = request.args.get('post_uuid')
    comments = comment_model.get_comment(post_uuid)
    return jsonify(comments), 200