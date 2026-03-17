"""
app/services/notification_service.py

Notification service for creating, retrieving, and managing user notifications.
Handles notification creation, read status, and cleanup of expired notifications.
"""

from datetime import datetime, timedelta
from app.models.notification import Notification
from app.core.extensions import  sio
from sqlalchemy.orm import Session
from app.core.database import get_db


class NotificationService:
    """Service for managing user notifications."""

    @staticmethod
    def create_notification(
        db: Session,
        user_id: int,
        title: str,
        message: str,
        type_: str = 'info',
        data: dict = None,
        action_url: str = None,
        icon: str = None,
        color: str = None,
        expires_in_days: int = 30,
    ) -> Notification:
        """
        Create a new notification for a user.
        """
        expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
        
        notification = Notification(
            db=db,
            user_id=user_id,
            type=type_,
            title=title,
            message=message,
            data=data,
            action_url=action_url,
            icon=icon,
            color=color,
            expires_at=expires_at,
        )
        
        db.add(notification)
        db.commit()
        
        # Emit real-time WebSocket event
        # Note: sio.emit is normally async. If calling from sync service, use a wrapper or the manager.
        # Since this is a domain service, we can use a thread-safe helper if needed.
        # However, for simplicity in migration, we'll try standard emit.
        try:
            # For ASGI SocketIO, we might need to use an async loop or background task
            # but usually sio.emit works if called from the same thread.
            import asyncio
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.create_task(sio.emit('notification', notification.to_dict(), room=f"user_{user_id}"))
                else:
                    asyncio.run(sio.emit('notification', notification.to_dict(), room=f"user_{user_id}"))
            except RuntimeError:
                # No event loop
                pass
        except Exception as e:
            print(f"SocketIO emit failed: {e}")

        return notification

    @staticmethod
    def get_user_notifications(
        db: Session, user_id: int, limit: int = 50, unread_only: bool = False) -> list:
        """Retrieve user's notifications."""
        query = db.query(Notification).filter_by(user_id=user_id)
        
        if unread_only:
            query = query.filter_by(read=False)
        
        notifications = query.order_by(Notification.created_at.desc()).limit(limit).all()
        return [n.to_dict() for n in notifications]

    @staticmethod
    def get_unread_count(db: Session, user_id: int) -> int:
        """Get count of unread notifications for a user."""
        return db.query(Notification).filter_by(user_id=user_id, read=False).count()

    @staticmethod
    def mark_as_read(db: Session, user_id: int, notification_id: int) -> bool:
        """Mark a single notification as read."""
        notification = db.query(Notification).filter_by(id=notification_id, user_id=user_id).first()
        if notification:
            notification.mark_as_read()
            db.commit()
            return True
        return False

    @staticmethod
    def mark_all_as_read(db: Session, user_id: int) -> int:
        """Mark all unread notifications as read. Returns count marked."""
        unread = db.query(Notification).filter_by(user_id=user_id, read=False).all()
        count = len(unread)
        
        for notification in unread:
            notification.mark_as_read()
        
        db.commit()
        return count

    @staticmethod
    def delete_notification(db: Session, user_id: int, notification_id: int) -> bool:
        """Delete a notification."""
        notification = db.query(Notification).filter_by(id=notification_id, user_id=user_id).first()
        if notification:
            db.delete(notification)
            db.commit()
            return True
        return False

    @staticmethod
    def clear_all_notifications(db: Session, user_id: int) -> int:
        """Delete all notifications for a user. Returns count deleted."""
        notifications = db.query(Notification).filter_by(user_id=user_id).all()
        count = len(notifications)
        
        for notification in notifications:
            db.delete(notification)
        
        db.commit()
        return count

    @staticmethod
    def cleanup_expired_notifications(db: Session) -> int:
        """Delete all expired notifications."""
        expired = db.query(Notification).filter(
            Notification.expires_at <= datetime.utcnow()
        ).all()
        
        count = len(expired)
        for notification in expired:
            db.delete(notification)
        
        db.commit()
        return count
