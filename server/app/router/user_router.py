from flask import Blueprint

user_bp = Blueprint("user", __name__)

@user_bp.route("/me")
def get_me():
    return {"msg": "user ok"}