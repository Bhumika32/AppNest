# app/models/user_quest.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class UserQuest(Base):
    __tablename__ = "user_quests"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quest_id = Column(Integer, ForeignKey("quests.id"), nullable=False)

    status = Column(String(20), default="PENDING")  # PENDING | COMPLETED | FAILED
    progress = Column(Integer, default=0)

    completed_at = Column(DateTime)

    user = relationship("User")
    quest = relationship("Quest")

    __table_args__ = (
        UniqueConstraint("user_id", "quest_id", name="uq_user_quest"),
        Index("idx_user_quest_status", "user_id", "status"),
    )

    def __repr__(self):
        return f"<UserQuest user={self.user_id} quest={self.quest_id} status={self.status}>"