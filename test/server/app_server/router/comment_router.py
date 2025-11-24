from flask import Blueprint, request, jsonify, session
from app_server import db
from app_server.model.comment_model import add_comment, get_comment

comment_bp = Blueprint("comment", __name__)

# 댓글 생성: POST /comment/create
@comment_bp.post("/create")
def post_comment():
    request_json = request.get_json()
    post_uuid = request_json.get("post_uuid")
    comment_content = request_json.get("comment_content")

    if "user_id" not in session:
        return {"result": "FAILED", "msg": "로그인이 필요합니다."}, 401

    add_comment(session["user_id"], post_uuid, comment_content)
    return {"result": "SUCCESS"}, 200


# 댓글 조회: GET /comment/list?post_uuid=...
@comment_bp.get("/list")
def get_comment_list():
    post_uuid = request.args.get("post_uuid")
    comments = get_comment(post_uuid)
    return jsonify(comments), 200
