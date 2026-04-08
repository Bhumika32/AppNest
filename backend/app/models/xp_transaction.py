# app/models/xp_transaction.py

from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class XPTransaction(Base):
    __tablename__ = "xp_transactions"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=True)

    xp_awarded = Column(Integer, nullable=False)
    # anti-duplicate protection
    unique_hash = Column(String(255), unique=True, index=True)

    # Why XP was given
    source = Column(String(50), nullable=False, index=True)  # game | quest | system | bonus

    # Optional description
    reason = Column(String(255))

    created_at = Column(DateTime, default=func.now(), index=True)

    # Relationships
    user = relationship("User", backref="xp_transactions")
    module = relationship("Module", backref="xp_transactions")

    __table_args__ = (
        Index("idx_xp_user_time", "user_id", "created_at"),
    )

    def __repr__(self):
        return f"<XPTransaction user={self.user_id} xp={self.xp_awarded} source={self.source}>"