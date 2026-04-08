from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.models.quest import Quest
from app.models.user_quest import UserQuest
from app.repositories.base_repository import BaseRepository

class QuestRepository(BaseRepository[Quest]):
    def __init__(self):
        super().__init__(Quest)

class UserQuestRepository(BaseRepository[UserQuest]):
    def __init__(self):
        super().__init__(UserQuest)

    def get_active_quests(self, db: Session, user_id: int) -> List[UserQuest]:
        return db.query(self.model).options(joinedload(self.model.quest)).filter(
            self.model.user_id == user_id,
            self.model.status == "PENDING"
        ).all()

    def get_user_quest(self, db: Session, user_id: int, quest_id: int) -> Optional[UserQuest]:
        return db.query(self.model).filter(
            self.model.user_id == user_id,
            self.model.quest_id == quest_id
        ).first()

quest_repository = QuestRepository()
user_quest_repository = UserQuestRepository()
