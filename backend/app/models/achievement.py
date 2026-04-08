# app/models/achievement.py

from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base


class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True)

    key = Column(String(100), unique=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)

    def __repr__(self):
        return f"<Achievement {self.key}>"