"""
app/services/notification_service.py

Notification service for creating, retrieving, and managing user notifications.
Handles notification creation, read status, and cleanup of expired notifications.
"""

from datetime import datetime, timedelta
from app.models.notification import Notification
from app.core.extensions import db


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
        
        Args:
            user_id: Target user ID
            title: Notification title
            message: Notification message
            type_: Type of notification ('achievement', 'game', 'credit', 'system', 'social', 'alert')
            data: Additional context data (JSON)
            action_url: URL to navigate to on click
            icon: Icon name (lucide-react icons)
            color: Color class (neon-blue, neon-pink, etc.)
            expires_in_days: Number of days before auto-deletion
        
        Returns:
            Created Notification object
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
        return notification

    @staticmethod
    def get_user_notifications(user_id: int, limit: int = 50, unread_only: bool = False) -> list:
        """
        Retrieve user's notifications.
        
        Args:
            user_id: User ID
            limit: Maximum number of notifications to retrieve
            unread_only: If True, only return unread notifications
        
        Returns:
            List of notification dictionaries
        """
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
        """Delete all expired notifications. Run as scheduled task."""
        expired = Notification.query.filter(
            Notification.expires_at <= datetime.utcnow()
        ).all()
        
        count = len(expired)
        for notification in expired:
            db.session.delete(notification)
        
        db.session.commit()
        return count

    @staticmethod
    def notify_game_completion(user_id: int, game_name: str, score: int, credits_awarded: int):
        """Send notification for game completion."""
        NotificationService.create_notification(
            user_id=user_id,
            title=f"🎮 {game_name} Complete!",
            message=f"You scored {score} points and earned {credits_awarded} credits!",
            type_='game',
            data={'game': game_name, 'score': score, 'credits': credits_awarded},
            icon='Trophy',
            color='neon-blue',
        )

    @staticmethod
    def notify_achievement_unlocked(user_id: int, achievement_name: str, description: str):
        """Send notification for achievement unlock."""
        NotificationService.create_notification(
            user_id=user_id,
            title=f"🏆 Achievement Unlocked!",
            message=f"{achievement_name}: {description}",
            type_='achievement',
            data={'achievement': achievement_name},
            icon='Star',
            color='neon-pink',
        )

    @staticmethod
    def notify_credits_awarded(user_id: int, amount: int, reason: str = "Activity"):
        """Send notification for credits awarded."""
        NotificationService.create_notification(
            user_id=user_id,
            title=f"✨ {amount} Credits Awarded!",
            message=f"You earned {amount} credits for {reason}.",
            type_='credit',
            data={'amount': amount, 'reason': reason},
            icon='Zap',
            color='neon-green',
        )

    @staticmethod
    def notify_system_announcement(user_id: int, announcement: str):
        """Send system announcement to a user."""
        NotificationService.create_notification(
            user_id=user_id,
            title="📢 System Announcement",
            message=announcement,
            type_='system',
            icon='AlertCircle',
            color='neon-yellow',
        )

    @staticmethod
    def broadcast_announcement(announcement: str, exclude_admin: bool = False):
        """Send system announcement to all users in batches."""
        from app.models.user import User
        from app.models.role import Role
        
        query = User.query
        if exclude_admin:
            admin_role = Role.query.filter_by(name='admin').first()
            if admin_role:
                query = query.filter(User.role_id != admin_role.id)
        
        batch_size = 500
        offset = 0
        expires_at = datetime.utcnow() + timedelta(days=30)
        
        while True:
            users_batch = query.offset(offset).limit(batch_size).all()
            if not users_batch:
                break
                
            notifications_to_add = []
            for user in users_batch:
                notification = Notification(
                    user_id=user.id,
                    type='system',
                    title="📢 System Announcement",
                    message=announcement,
                    icon='AlertCircle',
                    color='neon-yellow',
                    expires_at=expires_at
                )
                notifications_to_add.append(notification)
                
            db.session.bulk_save_objects(notifications_to_add)
            db.session.commit()
            
            offset += batch_size
