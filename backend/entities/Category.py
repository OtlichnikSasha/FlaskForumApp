from app_config import db
from sqlalchemy import Column, Integer, String


class Category(db.Model):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String(2500), nullable=False)
    views = Column(Integer, default=0, nullable=False)

    question_count = 0

    def __repr__(self):
        return f'<category {self.id}>'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
