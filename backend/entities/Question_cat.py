from app_config import db
from sqlalchemy import Column, Integer,ForeignKey
from sqlalchemy.orm import relationship

class Question_cat(db.Model):
    __tablename__ = 'question_cat'


    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    question_id = Column(Integer, ForeignKey('question.id'))

    category = relationship("Category", backref="question_cat")

    def __repr__(self):
        return f'<question_cat {self.id}>'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
