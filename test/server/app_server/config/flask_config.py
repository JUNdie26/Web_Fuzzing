import os
from dotenv import load_dotenv

# 프로젝트 루트(.env 있는 위치) 기준으로 로드
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DB_USER = os.getenv("DB_USER", "wbz")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "wkdguswhd0626!!")
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "wbz")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
