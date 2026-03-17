from sqlalchemy.orm import Session
from app.models.quest import Quest, UserQuest
from app.domain.progression_service import ProgressionService
from datetime import datetime
from typing import List

class QuestService:
    """
    Handles quest management, progress tracking, and fulfillment.
    """

    @staticmethod
    def get_active_quests(db: Session, user_id: int) -> List[UserQuest]:
        """
        Fetches all pending quests for a user.
        """
        return db.query(UserQuest).filter_by(user_id=user_id, status='PENDING').all()

    @staticmethod
    def process_module_completion(db: Session, user_id: int, module_key: str, score: int) -> List[UserQuest]:
        """
        Checks all pending quests for the user and updates progress.
        Fulfills quests that hit the target score.
        """
        pending_quests = QuestService.get_active_quests(db,  user_id)
        completed_this_turn = []

        for user_quest in pending_quests:
            quest = user_quest.quest
            if quest.module_key == module_key or quest.module_key is None:
                # Update progress if score beats target or accumulates (assuming score check for now)
                if score >= quest.target_score:
                    QuestService._fulfill_quest(db, user_id, user_quest)
                    completed_this_turn.append(user_quest)
        
        return completed_this_turn

    @staticmethod
    def _fulfill_quest(db: Session, user_id: int, user_quest: UserQuest):
        """
        Marks quest as completed and awards XP.
        """
        from app.domain.event_bus import EventBus, Events
        
        user_quest.status = 'COMPLETED'
        user_quest.progress = user_quest.quest.target_score
        user_quest.completed_at = datetime.utcnow()
        
        # Award XP for quest completion
        xp_result = ProgressionService.award_xp(
            user_id=user_id,
            module_id=None, # Quest-based XP
            base_reward=user_quest.quest.xp_reward,
            reason=f"Quest Completed: {user_quest.quest.title}"
        )
        
        # Fire internal event for audit/other services
        EventBus.publish(Events.QUEST_COMPLETED, {
            "user_id": user_id,
            "quest_id": user_quest.quest_id,
            "quest_title": user_quest.quest.title,
            "xp_reward": user_quest.quest.xp_reward
        })
        
        db.flush()

    @staticmethod
    def assign_quest(db: Session, user_id: int, quest_id: int) -> UserQuest:
        """
        Manually assign a quest to a user.
        """
        existing = db.query(UserQuest).filter_by(user_id=user_id, quest_id=quest_id).first()
        if existing:
            return existing
            
        new_uq = UserQuest(user_id=user_id, quest_id=quest_id)
        db.add(new_uq)
        db.flush()
        return new_uq
