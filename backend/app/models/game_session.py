# app/models/game_session.py

from sqlalchemy import Column, Integer, DateTime, ForeignKey, JSON, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class GameSession(Base):
    __tablename__ = "game_sessions"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False, index=True)

    score = Column(Integer, default=0, nullable=False)
    duration_seconds = Column(Integer)

    # structured instead of text
    meta = Column(JSON)

    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User")
    module = relationship("Module")

    __table_args__ = (
        Index("idx_game_user_module", "user_id", "module_id"),
    )

    def __repr__(self):
        return f"<GameSession user={self.user_id} module={self.module_id} score={self.score}>"