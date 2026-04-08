from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    type = Column(String(50), nullable=False)  # achievement | system | alert | social

    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)

    is_read = Column(Boolean, default=False, index=True)
    read_at = Column(DateTime)

    # extra context
    data = Column(JSON)

    action_url = Column(String(255))

    priority = Column(String(20), default="normal")  # low | normal | high

    created_at = Column(DateTime, server_default=func.now(), index=True)
    expires_at = Column(DateTime)

    user = relationship("User")

    __table_args__ = (
        Index("idx_notification_user_read", "user_id", "is_read"),
    )

    def __repr__(self):
        return f"<Notification user={self.user_id} type={self.type}>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "type": self.type,
            "title": self.title,
            "message": self.message,
            "is_read": self.is_read,
            "read_at": self.read_at.isoformat() if self.read_at else None,
            "data": self.data,
            "action_url": self.action_url,
            "priority": self.priority,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
        }
# # app/models/notification.py

# from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON, Index
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql import func

# from app.core.database import Base


# class Notification(Base):
#     __tablename__ = "notifications"

#     id = Column(Integer, primary_key=True)

#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

#     type = Column(String(50), nullable=False)  # achievement | system | alert | social

#     title = Column(String(255), nullable=False)
#     message = Column(Text, nullable=False)

#     is_read = Column(Boolean, default=False, index=True)
#     read_at = Column(DateTime)

#     # extra context
#     data = Column(JSON)

#     action_url = Column(String(255))

#     priority = Column(String(20), default="normal")  # low | normal | high

#     created_at = Column(DateTime, server_default=func.now(), index=True)
#     expires_at = Column(DateTime)

#     user = relationship("User")

#     __table_args__ = (
#         Index("idx_notification_user_read", "user_id", "is_read"),
#     )

#     def __repr__(self):
#         return f"<Notification user={self.user_id} type={self.type}>"
    
    