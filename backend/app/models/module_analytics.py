# app/models/module_analytics.py

from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class ModuleAnalytics(Base):
    __tablename__ = "module_analytics"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False, index=True)

    event_type = Column(String(50), nullable=False, index=True)  # e.g.
    # start | end | error | abandon | retry

    duration = Column(Integer)  # seconds

    created_at = Column(DateTime, server_default=func.now(), index=True)

    user = relationship("User")
    module = relationship("Module")

    __table_args__ = (
        Index("idx_module_event", "module_id", "event_type"),
    )