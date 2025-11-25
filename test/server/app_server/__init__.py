import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv

# 전역으로 쓸 DB / Migrate 객체
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    # .env 로드
    load_dotenv()

    app = Flask(__name__)

    # =========================
    # 기본 설정
    # =========================
    # 예: .env에 이미 이런 식으로 들어있음
    # SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:wbz@localhost:3308/wbz
    db_uri = os.getenv("SQLALCHEMY_DATABASE_URI")
    if not db_uri:
        # DB URI가 없으면 .env를 제대로 안 읽은 거라 바로 에러 내는 게 낫다
        raise RuntimeError("SQLALCHEMY_DATABASE_URI not set in .env")

    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # 세션용 시크릿 키 (없으면 대충 하나)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")

    # 디버그용 출력 (네가 보던 그 로그랑 동일한 느낌)
    print(f"🔍 DB URI: {db_uri}")
    print(f"🔍 PORT: {os.getenv('DB_PORT', '3306')}")

    # =========================
    # 확장 초기화
    # =========================
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, supports_credentials=True)

    # =========================
    # 블루프린트 등록
    # (※ 여기서 '한 번씩만' 등록)
    # =========================
    from .router.auth_router import auth_bp
    from .router.post_router import post_bp
    from .router.comment_router import comment_bp

    # 이름 중복 방지: auth_bp = Blueprint("auth", __name__) 이런 식으로
    # 각 router 파일에서 한 번만 선언되어 있어야 한다.
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(post_bp, url_prefix="/post")
    app.register_blueprint(comment_bp, url_prefix="/comment")

    # =========================
    # 헬스체크용 루트
    # =========================
    @app.route("/")
    def index():
        return "WBZ server OK"

    return app
