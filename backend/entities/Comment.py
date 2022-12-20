from app_config import db
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Comment(db.Model):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    question_id = Column(Integer, ForeignKey('question.id'))
    author_id = Column(Integer, ForeignKey('user.id'))
    text = Column(String(5000), nullable=False)
    author = relationship("User", backref='comment')

    def __repr__(self):
        return f'<comment {self.id}>'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
