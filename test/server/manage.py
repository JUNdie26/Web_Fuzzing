from app_server import create_app
from app_server.config.flask_config import Config

app = create_app()

print("🔍 DB URI:", Config.SQLALCHEMY_DATABASE_URI)
print("🔍 PORT:", Config.DB_PORT)


if __name__ == "__main__":
    # Flask가 뜨는 포트 (웹 서버 포트)
    # .env에 FLASK_RUN_PORT를 안 넣었으면 5000번 사용
    import os

    port = int(os.getenv("FLASK_RUN_PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
