from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from .config.flask_config import Config

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)

    # 환경 변수에서 이상한 걸 섞지 말고, Config만 사용
    app.config.from_object(Config)

    # 디버그용 출력
    print("🔍 DB URI:", app.config["SQLALCHEMY_DATABASE_URI"])
    print("🔍 PORT:", Config.DB_PORT)

    db.init_app(app)

    # 모델 임포트
    from .model.user_model import User
    from .model.post_model import Post
    from .model.comment_model import Comment

    with app.app_context():
        db.create_all()

    # 블루프린트 등록
    from .router.auth_router import auth_bp
    from .router.post_router import post_bp
    from .router.comment_router import comment_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(post_bp)
    app.register_blueprint(comment_bp, url_prefix="/comments")

    @app.route("/")
    def index():
        return "WBZ server OK"

    return app
