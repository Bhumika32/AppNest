#app/repositories/xp_transaction_repository.py
from typing import List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.models.xp_transaction import XPTransaction
from app.repositories.base_repository import BaseRepository


class XPTransactionRepository(BaseRepository[XPTransaction]):

    def __init__(self):
        super().__init__(XPTransaction)

    def exists_hash(self, db: Session, unique_hash: str) -> bool:
        return db.query(self.model.id).filter(
            self.model.unique_hash == unique_hash
        ).first() is not None

    def get_today_xp(self, db: Session, user_id: int) -> int:
        today = datetime.utcnow().date()

        result = db.query(func.sum(self.model.xp_awarded)).filter(
            self.model.user_id == user_id,
            func.date(self.model.created_at) == today
        ).scalar()

        return int(result or 0)

    def get_module_xp_today(self, db: Session, user_id: int, module_id: int) -> int:
        today = datetime.utcnow().date()

        result = db.query(func.sum(self.model.xp_awarded)).filter(
            self.model.user_id == user_id,
            self.model.module_id == module_id,
            func.date(self.model.created_at) == today
        ).scalar()

        return int(result or 0)

    # 🔥 REQUIRED FOR DASHBOARD
    def get_xp_history_last_7_days(self, db: Session, user_id: int):
        seven_days_ago = datetime.utcnow() - timedelta(days=7)

        return (
            db.query(
                func.date(self.model.created_at),
                func.sum(self.model.xp_awarded)
            )
            .filter(
                self.model.user_id == user_id,
                self.model.created_at >= seven_days_ago
            )
            .group_by(func.date(self.model.created_at))
            .order_by(func.date(self.model.created_at))
            .all()
        )