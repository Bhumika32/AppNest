from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.otp_token import OTPToken
from app.repositories.base_repository import BaseRepository

class OTPRepository(BaseRepository[OTPToken]):
    def __init__(self):
        super().__init__(OTPToken)

    def get_daily_count(self, db: Session, user_id: int, purpose: str, today_start: datetime) -> int:
        return db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.purpose == purpose,
            self.model.created_at >= today_start
        ).count()

    def invalidate_active_tokens(self, db: Session, user_id: int, purpose: str):
        db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.purpose == purpose,
            self.model.used.is_(False)
        ).update({"used": True}, synchronize_session=False)

    def get_latest_token(self, db: Session, user_id: int, purpose: str) -> Optional[OTPToken]:
        return db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.purpose == purpose
        ).order_by(self.model.created_at.desc()).first()

    def get_active_token_for_update(self, db: Session, user_id: int, purpose: str) -> Optional[OTPToken]:
        return db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.purpose == purpose,
            self.model.used.is_(False)
        ).order_by(self.model.created_at.desc()).with_for_update().first()

otp_repository = OTPRepository()
