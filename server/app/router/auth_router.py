# app/router/auth_router.py
from flask import Blueprint

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    return {"msg": "login ok"}
