"""
app/services/notification_service.py

Notification service for creating, retrieving, and managing user notifications.
Handles notification creation, read status, and cleanup of expired notifications.
"""

from datetime import datetime, timedelta
from app.models.notification import Notification
from app.core.extensions import db, socketio


class NotificationService:
    """Service for managing user notifications."""

    @staticmethod
    def create_notification(
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
        
        db.session.add(notification)
        db.session.commit()
        
        # Real-time WebSocket emission is now handled by ExperienceEngine to prevent duplication
        # try:
        #     socketio.emit(
        #         'notification', 
        #         notification.to_dict(), 
        #         room=f"user_{user_id}"
        #     )
        # except Exception as e:
        #     # SocketIO might not be initialized in some contexts (e.g., CLI)
        #     print(f"SocketIO emit failed: {e}")

        return notification

    @staticmethod
    def get_user_notifications(user_id: int, limit: int = 50, unread_only: bool = False) -> list:
        """Retrieve user's notifications."""
        query = Notification.query.filter_by(user_id=user_id)
        
        if unread_only:
            query = query.filter_by(read=False)
        
        notifications = query.order_by(Notification.created_at.desc()).limit(limit).all()
        return [n.to_dict() for n in notifications]

    @staticmethod
    def get_unread_count(user_id: int) -> int:
        """Get count of unread notifications for a user."""
        return Notification.query.filter_by(user_id=user_id, read=False).count()

    @staticmethod
    def mark_as_read(user_id: int, notification_id: int) -> bool:
        """Mark a single notification as read."""
        notification = Notification.query.filter_by(id=notification_id, user_id=user_id).first()
        if notification:
            notification.mark_as_read()
            db.session.commit()
            return True
        return False

    @staticmethod
    def mark_all_as_read(user_id: int) -> int:
        """Mark all unread notifications as read. Returns count marked."""
        unread = Notification.query.filter_by(user_id=user_id, read=False).all()
        count = len(unread)
        
        for notification in unread:
            notification.mark_as_read()
        
        db.session.commit()
        return count

    @staticmethod
    def delete_notification(user_id: int, notification_id: int) -> bool:
        """Delete a notification."""
        notification = Notification.query.filter_by(id=notification_id, user_id=user_id).first()
        if notification:
            db.session.delete(notification)
            db.session.commit()
            return True
        return False

    @staticmethod
    def clear_all_notifications(user_id: int) -> int:
        """Delete all notifications for a user. Returns count deleted."""
        notifications = Notification.query.filter_by(user_id=user_id).all()
        count = len(notifications)
        
        for notification in notifications:
            db.session.delete(notification)
        
        db.session.commit()
        return count

    @staticmethod
    def cleanup_expired_notifications() -> int:
        """Delete all expired notifications."""
        expired = Notification.query.filter(
            Notification.expires_at <= datetime.utcnow()
        ).all()
        
        count = len(expired)
        for notification in expired:
            db.session.delete(notification)
        
        db.session.commit()
        return count
