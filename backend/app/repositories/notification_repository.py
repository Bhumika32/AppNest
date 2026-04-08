# -----------------------------------------------------------------------------
# File: backend/app/repositories/notification_repository.py
#
# Description:
# Notification Repository (Production Safe)
#
# Fixes:
# - Added get_total_count (CRITICAL)
# - Added logging on failures
# - Prevent silent DB errors
# -----------------------------------------------------------------------------

from typing import List
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.notification import Notification
from app.repositories.base_repository import BaseRepository
import logging

logger = logging.getLogger(__name__)


class NotificationRepository(BaseRepository[Notification]):

    def __init__(self):
        super().__init__(Notification)

    # -----------------------------
    # FETCH USER NOTIFICATIONS
    # -----------------------------
    def get_user_notifications(
        self,
        db: Session,
        user_id: int,
        limit: int = 50,
        unread_only: bool = False
    ) -> List[Notification]:

        limit = min(limit, 100)

        query = db.query(self.model).filter(self.model.user_id == user_id)

        if unread_only:
            query = query.filter(self.model.read.is_(False))

        return query.order_by(self.model.created_at.desc()).limit(limit).all()

    # -----------------------------
    # TOTAL COUNT (🔥 FIX)
    # -----------------------------
    def get_total_count(self, db: Session, user_id: int) -> int:
        return db.query(self.model).filter(
            self.model.user_id == user_id
        ).count()

    # -----------------------------
    # UNREAD COUNT
    # -----------------------------
    def get_unread_count(self, db: Session, user_id: int) -> int:
        return db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.is_read.is_(False)
        ).count()

    # -----------------------------
    # MARK AS READ
    # -----------------------------
    def mark_as_read(self, db: Session, user_id: int, notification_id: int) -> bool:
        try:
            updated = db.query(self.model).filter(
                self.model.id == notification_id,
                self.model.user_id == user_id
            ).update({"read": True})

            return updated > 0

        except Exception:
            logger.exception("[MARK_AS_READ_FAILED]")
            return False

    # -----------------------------
    # MARK ALL AS READ
    # -----------------------------
    def mark_all_as_read(self, db: Session, user_id: int) -> int:
        try:
            return db.query(self.model).filter(
                self.model.user_id == user_id,
                self.model.is_read.is_(False)
            ).update({"read": True})

        except Exception:
            logger.exception("[MARK_ALL_READ_FAILED]")
            return 0

    # -----------------------------
    # DELETE SINGLE
    # -----------------------------
    def delete_notification(self, db: Session, user_id: int, notification_id: int) -> bool:
        try:
            deleted = db.query(self.model).filter(
                self.model.id == notification_id,
                self.model.user_id == user_id
            ).delete()

            return deleted > 0

        except Exception:
            logger.exception("[DELETE_NOTIFICATION_FAILED]")
            return False

    # -----------------------------
    # CLEAR ALL
    # -----------------------------
    def clear_all(self, db: Session, user_id: int) -> int:
        try:
            return db.query(self.model).filter(
                self.model.user_id == user_id
            ).delete()

        except Exception:
            logger.exception("[CLEAR_ALL_FAILED]")
            return 0

    # -----------------------------
    # CLEANUP EXPIRED
    # -----------------------------
    def cleanup_expired(self, db: Session) -> int:
        try:
            return db.query(self.model).filter(
                self.model.expires_at <= datetime.utcnow()
            ).delete()

        except Exception:
            logger.exception("[CLEANUP_FAILED]")
            return 0


notification_repository = NotificationRepository()
# from typing import List
# from sqlalchemy.orm import Session
# from datetime import datetime
# from app.models.notification import Notification
# from app.repositories.base_repository import BaseRepository
# import logging

# logger = logging.getLogger(__name__)

# class NotificationRepository(BaseRepository[Notification]):
#     def __init__(self):
#         super().__init__(Notification)

#     def get_user_notifications(self, db: Session, user_id: int, limit: int = 50, unread_only: bool = False) -> List[Notification]:
#         limit = min(limit, 100)
#         query = db.query(self.model).filter(self.model.user_id == user_id)
#         if unread_only:
#             query = query.filter(self.model.read.is_(False))
#         return query.order_by(self.model.created_at.desc()).limit(limit).all()

#     def get_unread_count(self, db: Session, user_id: int) -> int:
#         return db.query(self.model).filter(
#             self.model.user_id == user_id,
#             self.model.read.is_(False)
#         ).count()

#     def mark_as_read(self, db: Session, user_id: int, notification_id: int) -> bool:
#         try:
#             updated = db.query(self.model).filter(
#                 self.model.id == notification_id,
#                 self.model.user_id == user_id
#             ).update({"read": True})
#             return updated > 0
#         except Exception:
#             return False

#     def mark_all_as_read(self, db: Session, user_id: int) -> int:
#         try:
#             return db.query(self.model).filter(
#                 self.model.user_id == user_id,
#                 self.model.read.is_(False)
#             ).update({"read": True})
#         except Exception:
#             return 0

#     def delete_notification(self, db: Session, user_id: int, notification_id: int) -> bool:
#         try:
#             deleted = db.query(self.model).filter(
#                 self.model.id == notification_id,
#                 self.model.user_id == user_id
#             ).delete()
#             return deleted > 0
#         except Exception:
#             return False

#     def clear_all(self, db: Session, user_id: int) -> int:
#         try:
#             return db.query(self.model).filter(self.model.user_id == user_id).delete()
#         except Exception:
#             return 0

#     def cleanup_expired(self, db: Session) -> int:
#         try:
#             return db.query(self.model).filter(self.model.expires_at <= datetime.utcnow()).delete()
#         except Exception:
#             logger.exception("Cleanup expired notifications failed")
#             return 0

# notification_repository = NotificationRepository()
