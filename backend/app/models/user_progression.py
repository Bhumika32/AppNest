# app/models/user_progression.py

from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base
from datetime import datetime, date


class UserProgression(Base):
    __tablename__ = "user_progression"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False, index=True)

    total_xp = Column(Integer, default=0, nullable=False)
    level = Column(Integer, default=1, nullable=False)

    rank_title = Column(String(100), default="Apprentice")

    # 🔥 STREAK SYSTEM (carefully designed)
    streak_count = Column(Integer, default=0, nullable=False)
    last_activity_date = Column(DateTime, nullable=True, index=True)

    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationship
    user = relationship("User", back_populates="progression")

    def __repr__(self):
        return f"<UserProgression user={self.user_id} xp={self.total_xp} level={self.level}>"