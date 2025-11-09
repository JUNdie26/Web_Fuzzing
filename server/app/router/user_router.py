# app/router/user_router.py  (이름 user_model.py면 헷갈리니까 바꾸는 게 좋음)
from flask import Blueprint

user_bp = Blueprint("user", __name__)

@user_bp.route("/me")
def get_me():
    return {"msg": "user ok"}
