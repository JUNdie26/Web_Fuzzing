from flask import Blueprint, request, jsonify, session
from ..model import comment_model

comment_bp = Blueprint("comment", __name__)

# 프론트에서 서버로 데이터를 넘겨주는 것을 일단 JSON으로 넘겨준다고 가정
# API 엔드포인트는 변경하는게 좋아보임 -> /api/comment
# { user_uuid = ..., post_uuid = ..., comment_content = ... }
@comment_bp.route('/', methods=['POST'])
def post_comment():
    request_json = request.get_json()
    user_uuid = request_json['user_uuid']
    post_uuid = request_json['post_uuid']
    comment_content = request_json['comment_content']

    # 현재 로그인한 세션이 request의 user_uuid와 다른 경우
    if session['user_id'] != user_uuid:
        return {'result': 'FAILED'}, 401

    comment_model.add_comment(user_uuid, post_uuid, comment_content)
    return {'result': 'SUCCESS'}, 200

# 댓글 불러오기, 별도의 인증과정은 필요 없음
@comment_bp.route('/', methods=['GET'])
def get_comment():
    request_json = request.get_json()
    post_uuid = request_json['post_uuid']
    comments = comment_model.get_comment(post_uuid)
    return jsonify(comments), 200