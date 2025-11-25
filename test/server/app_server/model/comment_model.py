from datetime import datetime
from app_server import db


class Comment(db.Model):
    __tablename__ = "comment"

    comment_uuid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_uuid = db.Column(
        db.Integer,
        db.ForeignKey("user.user_uuid"),
        nullable=False,
    )
    post_uuid = db.Column(
        db.Integer,
        db.ForeignKey("post.post_uuid"),
        nullable=False,
    )
    comment_content = db.Column(db.Text, nullable=False)

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

    # 관계 (옵션, 있으면 나중에 편함)
    user = db.relationship(
        "User",
        backref=db.backref("comments", cascade="all,delete-orphan"),
    )
    post = db.relationship(
        "Post",
        backref=db.backref("comments", cascade="all,delete-orphan"),
    )

    def to_dict(self):
        return {
            "comment_uuid": self.comment_uuid,
            "user_uuid": self.user_uuid,
            "post_uuid": self.post_uuid,
            "comment_content": self.comment_content,
            "create_time": self.create_time.isoformat()
            if self.create_time
            else None,
            "update_time": self.update_time.isoformat()
            if self.update_time
            else None,
        }
