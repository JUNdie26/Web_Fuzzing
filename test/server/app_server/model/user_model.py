from datetime import datetime
from app_server import db

class User(db.Model):
    __tablename__ = "user"

    user_uuid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(45), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(45), nullable=False)

    create_time = db.Column(
        db.DateTime,
        default=datetime.utcnow,          # 중요: datetime.utcnow() 말고 utcnow 함수 자체 넣어야 함
        nullable=False
    )

    update_time = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,         # 업데이트 시 자동 변경
        nullable=False
    )

    def to_dict(self):
        return {
            "user_uuid": self.user_uuid,
            "user_id": self.user_id,
            "name": self.name,
            "create_time": self.create_time,
            "update_time": self.update_time,
        }
