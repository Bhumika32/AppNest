# app/models/otp_token.py

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base
from datetime import datetime


class OTPToken(Base):
    __tablename__ = "otp_tokens"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    otp_hash = Column(String(255), nullable=False)

    purpose = Column(String(50), nullable=False)  # VERIFY_EMAIL | RESET_PASSWORD

    expires_at = Column(DateTime, nullable=False, index=True)

    used = Column(Boolean, default=False, nullable=False)

    # 🔥 security addition
    attempts = Column(Integer, default=0, nullable=False)

    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    user = relationship(
        "User",
        back_populates="otp_tokens"
    )

    __table_args__ = (
        Index("idx_otp_user_purpose", "user_id", "purpose"),
    )

    def is_expired(self):
        return datetime.utcnow() > self.expires_at

    def __repr__(self):
        return f"<OTPToken user={self.user_id} purpose={self.purpose}>"