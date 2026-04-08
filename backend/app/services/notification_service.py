# -----------------------------------------------------------------------------
# File: backend/app/services/notification_service.py
#
# Description:
# Stateless Notification Service
#
# Responsibilities:
# - Create notifications
# - Emit real-time socket events
# - Fetch notifications
# - Manage read/unread state
# - Provide notification statistics
#
# Production Improvements:
# - Added missing get_notification_stats (CRITICAL FIX)
# - Consistent commit/rollback handling
# - Safe async socket emission
# - Better logging
# -----------------------------------------------------------------------------

from datetime import datetime, timedelta
from typing import List, Dict
import logging
import asyncio

from sqlalchemy.orm import Session

from app.core.extensions import sio
from app.repositories.notification_repository import notification_repository

logger = logging.getLogger(__name__)


class NotificationService:

    # -----------------------------
    # CREATE NOTIFICATION
    # -----------------------------
    @staticmethod
    def create_notification(
        db: Session,
        user_id: int,
        title: str,
        message: str,
        type_: str = "info",
        data: dict = None,
        action_url: str = None,
        # icon: str = None,
        # color: str = None,
        expires_in_days: int = 30
    ):
        print("CREATING NOTIFICATION")
        try:
            expires_at = datetime.utcnow() + timedelta(days=expires_in_days)

            notification = notification_repository.create(db, {
                "user_id": user_id,
                "type": type_,
                "title": title,
                "message": message,
                "data": data,
                "action_url": action_url,
                # "icon": icon,
                # "color": color,
                "expires_at": expires_at
            })

            db.commit()
            db.refresh(notification)

            # Emit real-time event
            NotificationService._emit_notification(
                user_id,
                notification.to_dict()
            )

            return notification

        except Exception:
            db.rollback()
            logger.exception("[NOTIFICATION_CREATE_FAILED]")
            raise

    # -----------------------------
    # SOCKET EMISSION
    # -----------------------------
    @staticmethod
    def _emit_notification(user_id: int, payload: dict):
        room = f"user_{user_id}"
        print("EMITTING SOCKET EVENT")
        async def emit():
            try:
                await sio.emit("notification", payload, room=room)
            except Exception as e:
                logger.warning(f"[SOCKET_EMIT_FAILED] {e}")

        try:
            loop = asyncio.get_running_loop()
            loop.create_task(emit())
        except RuntimeError:
            asyncio.run(emit())

    # -----------------------------
    # FETCH NOTIFICATIONS
    # -----------------------------
    @staticmethod
    def get_user_notifications(
        db: Session,
        user_id: int,
        limit: int = 50,
        unread_only: bool = False
    ) -> List[Dict]:

        notifications = notification_repository.get_user_notifications(
            db, user_id, limit, unread_only
        )

        return [n.to_dict() for n in notifications]

    # -----------------------------
    # UNREAD COUNT
    # -----------------------------
    @staticmethod
    def get_unread_count(db: Session, user_id: int) -> int:
        return notification_repository.get_unread_count(db, user_id)

    # -----------------------------
    # 🔥 FIXED: NOTIFICATION STATS
    # -----------------------------
    @staticmethod
    def get_notification_stats(db: Session, user_id: int) -> Dict:
        """
        Returns:
        {
            total: int,
            unread: int
        }
        """

        try:
            total = notification_repository.get_total_count(db, user_id)
            unread = notification_repository.get_unread_count(db, user_id)

            return {
                "total": total,
                "unread": unread
            }

        except Exception:
            logger.exception("[NOTIFICATION_STATS_FAILED]")
            raise

    # -----------------------------
    # MARK AS READ
    # -----------------------------
    @staticmethod
    def mark_as_read(db: Session, user_id: int, notification_id: int) -> bool:
        try:
            result = notification_repository.mark_as_read(
                db, user_id, notification_id
            )

            if result:
                db.commit()
            else:
                db.rollback()

            return result

        except Exception:
            db.rollback()
            logger.exception("[MARK_AS_READ_FAILED]")
            raise

    # -----------------------------
    # MARK ALL AS READ
    # -----------------------------
    @staticmethod
    def mark_all_as_read(db: Session, user_id: int) -> int:
        try:
            count = notification_repository.mark_all_as_read(db, user_id)
            db.commit()
            return count

        except Exception:
            db.rollback()
            logger.exception("[MARK_ALL_READ_FAILED]")
            raise

    # -----------------------------
    # DELETE SINGLE
    # -----------------------------
    @staticmethod
    def delete_notification(db: Session, user_id: int, notification_id: int) -> bool:
        try:
            result = notification_repository.delete_notification(
                db, user_id, notification_id
            )

            if result:
                db.commit()
            else:
                db.rollback()

            return result

        except Exception:
            db.rollback()
            logger.exception("[DELETE_NOTIFICATION_FAILED]")
            raise

    # -----------------------------
    # CLEAR ALL
    # -----------------------------
    @staticmethod
    def clear_all_notifications(db: Session, user_id: int) -> int:
        try:
            count = notification_repository.clear_all(db, user_id)
            db.commit()
            return count

        except Exception:
            db.rollback()
            logger.exception("[CLEAR_NOTIFICATIONS_FAILED]")
            raise

    # -----------------------------
    # CLEANUP EXPIRED
    # -----------------------------
    @staticmethod
    def cleanup_expired_notifications(db: Session) -> int:
        try:
            count = notification_repository.cleanup_expired(db)
            db.commit()
            return count

        except Exception:
            db.rollback()
            logger.exception("[CLEANUP_FAILED]")
            raise
# from datetime import datetime, timedelta
# from typing import List, Dict
# import logging
# import asyncio

# from sqlalchemy.orm import Session
# from app.core.extensions import sio
# from app.repositories.notification_repository import notification_repository

# logger = logging.getLogger(__name__)

# class NotificationService:

#     @staticmethod
#     def create_notification(
#         db: Session, user_id: int, title: str, message: str,
#         type_: str = "info", data: dict = None, action_url: str = None,
#         icon: str = None, color: str = None, expires_in_days: int = 30
#     ):
#         try:
#             expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
#             notification = notification_repository.create(db, {
#                 "user_id": user_id, "type": type_, "title": title,
#                 "message": message, "data": data, "action_url": action_url,
#                 "icon": icon, "color": color, "expires_at": expires_at
#             })
            
#             NotificationService._emit_notification(user_id, notification.to_dict())
#             return notification
#         except Exception:
#             db.rollback()
#             logger.exception("Notification creation failed")
#             raise

#     @staticmethod
#     def _emit_notification(user_id: int, payload: dict):
#         room = f"user_{user_id}"
#         async def emit():
#             try:
#                 await sio.emit("notification", payload, room=room)
#             except Exception as e:
#                 logger.warning(f"Socket emit failed: {e}")

#         try:
#             loop = asyncio.get_running_loop()
#             loop.create_task(emit())
#         except RuntimeError:
#             asyncio.run(emit())

#     @staticmethod
#     def get_user_notifications(db: Session, user_id: int, limit: int = 50, unread_only: bool = False) -> List[Dict]:
#         notifications = notification_repository.get_user_notifications(db, user_id, limit, unread_only)
#         return [n.to_dict() for n in notifications]

#     @staticmethod
#     def get_unread_count(db: Session, user_id: int) -> int:
#         return notification_repository.get_unread_count(db, user_id)

#     @staticmethod
#     def mark_as_read(db: Session, user_id: int, notification_id: int) -> bool:
#         result = notification_repository.mark_as_read(db, user_id, notification_id)
#         if result: db.commit()
#         else: db.rollback()
#         return result

#     @staticmethod
#     def mark_all_as_read(db: Session, user_id: int) -> int:
#         count = notification_repository.mark_all_as_read(db, user_id)
#         db.commit()
#         return count

#     @staticmethod
#     def delete_notification(db: Session, user_id: int, notification_id: int) -> bool:
#         result = notification_repository.delete_notification(db, user_id, notification_id)
#         if result: db.commit()
#         else: db.rollback()
#         return result

#     @staticmethod
#     def clear_all_notifications(db: Session, user_id: int) -> int:
#         count = notification_repository.clear_all(db, user_id)
#         db.commit()
#         return count

#     @staticmethod
#     def cleanup_expired_notifications(db: Session) -> int:
#         count = notification_repository.cleanup_expired(db)
#         db.commit()
#         return count
