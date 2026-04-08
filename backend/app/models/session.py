# app/models/session.py

from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, func, Index
from sqlalchemy.orm import relationship
from app.core.database import Base

import uuid
from datetime import datetime


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    refresh_token_hash = Column(String(255), unique=True, nullable=False)

    device_info = Column(String(255))
    ip_address = Column(String(45))

    expires_at = Column(DateTime, nullable=False, index=True)
    revoked = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime, server_default=func.now())
    last_used_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationship
    user = relationship("User", back_populates="sessions")

    # Index for performance
    __table_args__ = (
        Index("idx_session_user_active", "user_id", "revoked"),
        Index("idx_session_user", "user_id"),
        Index("idx_session_active", "revoked"),
    )

    def is_expired(self) -> bool:
        return datetime.utcnow() > self.expires_at

    def __repr__(self):
        return f"<Session {self.id} user={self.user_id}>"