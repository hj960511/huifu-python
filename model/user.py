# model/user.py
from core.mysql_core import db
from base.model_base import BaseModel

class User(BaseModel):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer)

    def __repr__(self):
        return f'<User {self.name}>'

