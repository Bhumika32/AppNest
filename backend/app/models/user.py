# app/models/user.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base
from werkzeug.security import generate_password_hash, check_password_hash


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(120), unique=True, nullable=False, index=True)

    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    password_hash = Column(String(255), nullable=False)

    is_verified = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)  # 🔥 important

   

    avatar_url = Column(String(255))
    bio = Column(String(500))

    created_at = Column(DateTime, server_default=func.now())
    deleted_at = Column(DateTime)
    last_login_at = Column(DateTime, index=True)  # 🔥 important

    # Relationships
    role = relationship("Role", back_populates="users")
    sessions = relationship("Session", cascade="all, delete-orphan")
    otp_tokens = relationship("OTPToken", back_populates="user", cascade="all, delete-orphan")
    progression = relationship("UserProgression", uselist=False, back_populates="user")
    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)