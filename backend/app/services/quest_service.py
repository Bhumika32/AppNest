from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
import logging

from app.models.quest import Quest
from app.services.progression_service import ProgressionService
from app.domain.event_bus import EventBus, Events
from app.repositories.quest_repository import quest_repository, user_quest_repository

logger = logging.getLogger(__name__)

class QuestService:

    @staticmethod
    def get_active_quests(db: Session, user_id: int) -> List:
        return user_quest_repository.get_active_quests(db, user_id)

    @staticmethod
    def process_module_completion(db: Session, user_id: int, module_id: int, score: int) -> List:
        completed = []
        try:
            quests = QuestService.get_active_quests(db, user_id)
            for uq in quests:
                quest = uq.quest
                if not quest:
                    continue

                if quest.module_id and quest.module_id != module_id:
                    continue

                if uq.status == "COMPLETED":
                    continue

                uq.progress = max(uq.progress or 0, score)
                if uq.progress >= quest.target_score:
                    QuestService._fulfill_quest(db, user_id, uq)
                    completed.append(uq)
            db.commit()
        except Exception:
            db.rollback()
            logger.exception("Quest processing failed")

        return completed

    @staticmethod
    def _fulfill_quest(db: Session, user_id: int, uq):
        if uq.status == "COMPLETED":
            return
        quest = uq.quest
        
        user_quest_repository.update(db, uq, {
            "status": "COMPLETED",
            "progress": quest.target_score,
            "completed_at": datetime.utcnow()
        })

        ProgressionService.award_xp(
            db=db,
            user_id=user_id,
            module_id=None,
            base_reward=quest.xp_reward,
            reason=f"Quest Completed: {quest.title}"
        )

        EventBus.publish(Events.QUEST_COMPLETED, {
            "db": db,
            "user_id": user_id,
            "quest_id": uq.quest_id,
            "quest_title": quest.title,
            "xp_reward": quest.xp_reward
        })

    @staticmethod
    def assign_quest(db: Session, user_id: int, quest_id: int):
        try:
            existing = user_quest_repository.get_user_quest(db, user_id, quest_id)
            if existing: return existing

            quest = quest_repository.get_by_id(db, quest_id)
            if not quest: raise ValueError("Quest not found")

            uq = user_quest_repository.create(db, {
                "user_id": user_id,
                "quest_id": quest_id,
                "status": "PENDING",
                "progress": 0
            })
            return uq
        except Exception:
            db.rollback()
            logger.exception("Assign quest failed")
            raise
