from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)

    def get_by_email_or_username(self, db: Session, email: str, username: str) -> Optional[User]:
        return db.query(self.model).filter(
            (self.model.email == email) | (self.model.username == username)
        ).first()

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(self.model).filter(self.model.email == email).first()

    def get_active_user_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(self.model).filter(
            self.model.email == email,
            self.model.deleted_at.is_(None)
        ).first()

    def get_by_email_for_update(self, db: Session, email: str) -> Optional[User]:
        return db.query(self.model).filter(
            self.model.email == email
        ).with_for_update().first()

user_repository = UserRepository()

