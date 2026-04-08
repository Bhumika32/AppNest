# app/models/module.py

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, JSON, Index, Enum
from sqlalchemy.sql import func
from app.core.database import Base


class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True)

    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False, index=True)

    # 🔥 enforce control
    type = Column(Enum("game", "tool", name="module_type"), nullable=False)

    description = Column(Text)

    icon = Column(String(50))
    thumbnail = Column(String(255))

    component_key = Column(String(100), nullable=False)

    category = Column(String(50))
    difficulty = Column(String(50))

    is_active = Column(Boolean, default=True, nullable=False)

    capabilities = Column(JSON)

    xp_reward_base = Column(Integer, default=10)

    created_at = Column(DateTime, server_default=func.now())

    __table_args__ = (
        Index("idx_module_type_active", "type", "is_active"),
    )

    def __repr__(self):
        return f"<Module {self.slug} type={self.type}>"