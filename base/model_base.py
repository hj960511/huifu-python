from core.mysql_core import db

class BaseModel(db.Model):
    __abstract__ = True  # 抽象类

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id_):
        return cls.query.get(id_)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        instance.save()
        return instance

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()
