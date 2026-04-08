#app/repositories/progression_repository.py
from sqlalchemy.orm import Session
from app.models.user_progression import UserProgression
from app.repositories.base_repository import BaseRepository


class ProgressionRepository(BaseRepository[UserProgression]):

    def __init__(self):
        super().__init__(UserProgression)

    def get_by_user_id_for_update(self, db: Session, user_id: int):
        """
        CRITICAL: prevents race conditions
        """
        return db.query(self.model).filter(
            self.model.user_id == user_id
        ).with_for_update().first()

    def get_by_user_id(self, db: Session, user_id: int):
        return db.query(self.model).filter(
            self.model.user_id == user_id
        ).first()