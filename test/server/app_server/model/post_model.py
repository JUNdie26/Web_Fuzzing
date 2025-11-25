from datetime import datetime
from app_server import db


class Post(db.Model):
    __tablename__ = "post"

    post_uuid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_uuid = db.Column(
        db.Integer,
        db.ForeignKey("user.user_uuid"),
        nullable=False,
    )
    post_title = db.Column(db.String(45), nullable=False)
    post_content = db.Column(db.Text, nullable=False)

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

    user = db.relationship(
        "User",
        backref=db.backref("posts", cascade="all,delete-orphan"),
    )

    def to_dict(self):
        return {
            "post_uuid": self.post_uuid,
            "user_uuid": self.user_uuid,
            "post_title": self.post_title,
            "post_content": self.post_content,
            "create_time": self.create_time.isoformat()
            if self.create_time
            else None,
            "update_time": self.update_time.isoformat()
            if self.update_time
            else None,
        }
