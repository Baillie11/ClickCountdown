# app/models/countdown_models.py

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app import db


class Countdown(db.Model):
    __tablename__ = 'countdowns'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    title = Column(String(100), nullable=False)
    target_datetime = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_public = Column(Boolean, default=False)

    user = relationship('User', backref='countdowns')

    def __repr__(self):
        return f"<Countdown '{self.title}' - Ends {self.target_datetime}>"
