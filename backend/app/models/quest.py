# app/models/quest.py

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.core.database import Base



class Quest(Base):
    __tablename__ = "quests"

    id = Column(Integer, primary_key=True)

    title = Column(String(100), nullable=False)
    description = Column(Text)

    module_id = Column(Integer, ForeignKey("modules.id"), index=True)  

    target_value = Column(Integer, default=0)
    xp_reward = Column(Integer, default=50)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<Quest {self.title}>"