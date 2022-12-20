from app_config import db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship


class Question(db.Model):
    __tablename__ = 'question'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String(1000), nullable=False)
    text = Column(String(7000), nullable=False)
    views = Column(Integer, default=0, nullable=False)
    author_id = Column(Integer, ForeignKey('user.id'))
    start_date = Column(DateTime, default=datetime.utcnow, nullable=False)



    categories = relationship("Question_cat", backref="question")
    comments = relationship("Comment", backref="question")
    author = relationship("User", backref='question')
    cats = []
    comment_count = 0
    question_count = 0

    def __repr__(self):
        return f'<question {self.id}>'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
