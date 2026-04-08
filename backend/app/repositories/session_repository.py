from typing import Optional
from sqlalchemy.orm import Session
from app.models.session import Session as UserSession
from app.repositories.base_repository import BaseRepository

class SessionRepository(BaseRepository[UserSession]):
    def __init__(self):
        super().__init__(UserSession)

    def revoke_active_sessions(self, db: Session, user_id: int):
        db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.revoked.is_(False)
        ).update({"revoked": True})
        
    def revoke_all_sessions(self, db: Session, user_id: int):
        db.query(self.model).filter(
            self.model.user_id == user_id
        ).update({"revoked": True})
        db.commit()

session_repository = SessionRepository()
