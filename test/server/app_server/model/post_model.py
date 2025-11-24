from datetime import datetime
from app_server import db

class Post(db.Model):
    __tablename__ = "post"

    post_uuid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(45), nullable=False)       # ★ 수정됨 ★
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
