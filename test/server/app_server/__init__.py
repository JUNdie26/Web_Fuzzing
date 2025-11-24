from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .config.flask_config import Config

db = SQLAlchemy()

def create_app():
    import os
    print("🔍 DB URI:", os.getenv("SQLALCHEMY_DATABASE_URI"))
    print("🔍 PORT:", os.getenv("DB_PORT"))

    app = Flask(__name__)
    app.config.from_object(Config)

    # DB 초기화
    db.init_app(app)

    # CORS 허용 (React 연동)
    CORS(app, supports_credentials=True)

    # 🔥 라우터는 한 번만 import
    from .router.auth_router import auth_bp
    from .router.user_router import user_bp
    from .router.comment_router import comment_bp
    from .router.post_router import post_bp

    # 🔥 Blueprint도 한 번만 등록
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/users")
    app.register_blueprint(comment_bp, url_prefix="/comment")
    app.register_blueprint(post_bp, url_prefix="/post")

    # DB 테이블 생성
    with app.app_context():
        from .model import User, Post, Comment
        db.create_all()

    return app
