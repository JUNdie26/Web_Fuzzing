from datetime import datetime
from app_server import db


class User(db.Model):
    __tablename__ = "user"

    user_uuid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(45), unique=True, nullable=False)
    user_password = db.Column(db.String(45), nullable=False)
    user_name = db.Column(db.String(45), nullable=False)

    create_time = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    update_time = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    def to_dict(self):
        return {
            "user_uuid": self.user_uuid,
            "user_id": self.user_id,
            "user_name": self.user_name,
            "create_time": self.create_time.isoformat()
            if self.create_time
            else None,
            "update_time": self.update_time.isoformat()
            if self.update_time
            else None,
        }
