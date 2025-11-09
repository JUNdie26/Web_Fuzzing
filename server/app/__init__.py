from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .config.flask_config import Config

# SQLAlchemy 전역 객체
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # DB 초기화
    db.init_app(app)

    # CORS 허용 (React 연동용)
    CORS(app, supports_credentials=True)

    # 블루프린트 등록
    from .router.auth_router import auth_bp
    from .router.user_router import user_bp  # 파일명이 user_model.py라 user_router.py로 바꾸는 게 나음
    # post_router, comment_router 추가 시 아래처럼
    # from .router.post_router import post_bp
    # from .router.comment_router import comment_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(user_bp, url_prefix="/api/users")
    # app.register_blueprint(post_bp, url_prefix="/api/posts")

    # DB 테이블 생성 (개발 단계에서만)
    with app.app_context():
        from .model import User, Post, Comment
        db.create_all()

    return app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .config.flask_config import Config

# SQLAlchemy 전역 객체
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # DB 초기화
    db.init_app(app)

    # CORS 허용 (React 연동용)
    CORS(app, supports_credentials=True)

    # 블루프린트 등록
    from .router.auth_router import auth_bp
    from .router.user_router import user_bp  # 파일명이 user_model.py라 user_router.py로 바꾸는 게 나음
    # post_router, comment_router 추가 시 아래처럼
    # from .router.post_router import post_bp
    # from .router.comment_router import comment_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(user_bp, url_prefix="/api/users")
    # app.register_blueprint(post_bp, url_prefix="/api/posts")

    # DB 테이블 생성 (개발 단계에서만)
    with app.app_context():
        from .model import User, Post, Comment
        db.create_all()

    return app
