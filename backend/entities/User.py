from app_config import db
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
class User(db.Model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    login = Column(String(1024), nullable=False)
    password = Column(String(1024), nullable=False)
    registration_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    description = Column(String(5000), nullable=False)
    author_comment = relationship("Comment", backref='user')

    comment_count = 0
    statistics = {}

    def __repr__(self):
        return f'<user {self.id}>'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
