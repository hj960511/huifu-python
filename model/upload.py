# model/upload_core.py
from datetime import datetime
from core.mysql_core import db

from base.model_base import BaseModel

class Upload(BaseModel):
    __tablename__ = 'upload'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(100), nullable=False)
    size = db.Column(db.Integer, nullable=False)  # 单位：字节
    md5 = db.Column(db.String(32), unique=True, nullable=False)
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)
    absolute_path = db.Column(db.String(512), nullable=False)
    unique_filename = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Upload {self.filename}>"
