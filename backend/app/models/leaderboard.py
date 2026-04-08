# app/models/leaderboard.py

from sqlalchemy import Column, Integer, DateTime, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint

__table_args__ = (
    Index("idx_leaderboard_module_score", "module_id", "top_score"),
    UniqueConstraint("user_id", "module_id", name="uq_user_module_score"),
)

from app.core.database import Base

class Leaderboard(Base):
    __tablename__ = "leaderboards"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False, index=True)

    top_score = Column(Integer, default=0, nullable=False)

    last_updated = Column(DateTime, default=func.now(), onupdate=func.now())

    user = relationship("User")
    module = relationship("Module")

    __table_args__ = (
    Index("idx_leaderboard_module_score", "module_id", "top_score"),
    UniqueConstraint("user_id", "module_id", name="uq_user_module_score"),
    )

    def __repr__(self):
        return f"<Leaderboard user={self.user_id} module={self.module_id} score={self.top_score}>"