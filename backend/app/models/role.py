# app/models/role.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)

    # e.g. USER, ADMIN, SUPER_ADMIN
    name = Column(String(50), unique=True, nullable=False)

    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    users = relationship("User", back_populates="role")

    def __repr__(self):
        return f"<Role {self.name}>"