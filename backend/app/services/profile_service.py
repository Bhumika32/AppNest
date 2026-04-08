from dataclasses import dataclass
from typing import Optional, Dict, List
import logging
from sqlalchemy.orm import Session
from app.domain.profile_domain import ProfileDomain
from app.repositories.base_repository import BaseRepository
logger = logging.getLogger(__name__)
from app.repositories.module_repository import ModuleRepository

@dataclass
class UserProfileDTO:
    id: int
    username: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    avatar_url: Optional[str]
    bio: Optional[str]
    joined_date: str


class UserProfileService:

    def __init__(
        self,
        user_repo,
        session_repo,
        progression_repo,
        xp_repo,
        module_repo
    ):
        self.user_repo = user_repo
        self.session_repo = session_repo
        self.progression_repo = progression_repo
        self.xp_repo = xp_repo
        self.module_repo = module_repo

    # -----------------------------
    # PROFILE
    # -----------------------------
    def get_profile(self, db: Session, user_id: int) -> UserProfileDTO:
        user = self.user_repo.get_by_id(db, user_id)

        if not user:
            raise ValueError("User not found")

        return UserProfileDTO(
            id=user.id,
            username=user.username or user.email.split("@")[0],
            email=user.email,
            first_name=getattr(user, "first_name", None),
            last_name=getattr(user, "last_name", None),
            avatar_url=getattr(user, "avatar_url", None),
            bio=getattr(user, "bio", None),
            joined_date=user.created_at.strftime("%Y-%m-%d") if user.created_at else ""
        )

    # -----------------------------
    # UPDATE PROFILE (WITH TX CONTROL)
    # -----------------------------
    def update_profile(self, db: Session, user_id: int, data: Dict):
        allowed = {"first_name", "last_name", "bio"}

        update_data = {k: v for k, v in data.items() if k in allowed}

        try:
            user = self.user_repo.get_by_id(db, user_id)
            self.user_repo.update(db, user, update_data)
            db.commit()
            # with db.begin():
            #     user = self.user_repo.get_by_id(db, user_id)
            #     self.user_repo.update(db, user, update_data)
        except Exception:
            logger.exception("Profile update failed")
            raise

    # -----------------------------
    # STATISTICS (ORCHESTRATION ONLY)
    # -----------------------------
    def get_statistics(self, db: Session, user_id: int) -> Dict:

        games, tools = self.session_repo.get_counts_by_module_type(db, user_id)
        progression = self.progression_repo.get_by_user_id(db, user_id)

        xp_rows = self.xp_repo.get_xp_history_last_7_days(db, user_id)

        performance = ProfileDomain.build_performance_history(xp_rows)
        account_age = ProfileDomain.calculate_account_age(
            getattr(progression, "created_at", None)
        )

        return {
            "games_played": games,
            "tools_used": tools,
            "total_roasts": 0,
            "account_age_days": account_age,
            "credits": int(getattr(progression, "credits", 0) or 0),
            "xp": int(getattr(progression, "total_xp", 0) or 0),
            "level": int(getattr(progression, "level", 1) or 1),
            "performance_history": performance
        }

    # # -----------------------------
    # # RECENT ACTIVITY (DTO SAFE)
    # # -----------------------------
    # def get_recent_activity(self, db: Session, user_id: int) -> List[Dict]:
    #     rows = self.session_repo.get_recent_sessions(db, user_id)

    #     return rows

    # -----------------------------
    # RECENT ACTIVITY (DTO SAFE)
    # -----------------------------
    def get_recent_activity(self, db: Session, user_id: int) -> List[Dict]:

        rows = self.session_repo.get_recent_sessions(db, user_id)

        activity = []

        for r in rows:

            module = self.module_repo.get_by_id(db, r.module_id)

            activity.append({
                "type": module.type,   # "game" or "tool"
                "description": f"Used {module.name}",
                "module": module.name,
                "score": r.score,
                "dare": r.created_at.isoformat() if r.created_at else None
            })

        return activity

    # -----------------------------
    # ACHIEVEMENTS (PURE LOGIC)
    # -----------------------------
    def get_achievements(self, stats: Dict) -> List[str]:
        achievements = []

        if stats["games_played"] >= 1:
            achievements.append("First Game")

        if stats["games_played"] >= 10:
            achievements.append("Game Enthusiast")

        if stats["tools_used"] >= 1:
            achievements.append("Tool Explorer")

        return achievements
