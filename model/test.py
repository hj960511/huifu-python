# model/test.py
from core.mysql_core import db
from base.model_base import BaseModel


class Test(BaseModel):
    __tablename__ = 'test'  # 数据库表名

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Test {self.name}>'
