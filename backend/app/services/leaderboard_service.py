# File: app/services/leaderboard_service.py

from typing import Optional, List, Dict
from datetime import datetime
import logging

from sqlalchemy.orm import Session

from app.models.leaderboard import Leaderboard
from app.models.user import User
from app.models.user_progression import UserProgression

from app.core.cache_service import CacheService
from app.repositories.leaderboard_repository import leaderboard_repository

logger = logging.getLogger(__name__)


class LeaderboardService:

    # -----------------------------
    # UPDATE SCORE
    # -----------------------------
    @staticmethod
    def update_score(
        db: Session,
        user_id: int,
        module_id: int,
        score: int
    ) -> Optional[Leaderboard]:

        try:
            entry = leaderboard_repository.get_user_score_for_update(
                db, user_id, module_id
            )

            if not entry:
                entry = leaderboard_repository.create(db, {
                    "user_id": user_id,
                    "module_id": module_id,
                    "top_score": score,
                    "last_updated": datetime.utcnow()
                })

            elif score > entry.top_score:
                leaderboard_repository.update(db, entry, {
                    "top_score": score,
                    "last_updated": datetime.utcnow()
                })

            LeaderboardService._invalidate_cache(module_id)

            return entry

        except Exception:
            db.rollback()
            logger.exception(
                f"Leaderboard update failed user={user_id} module={module_id}"
            )
            return None

    # -----------------------------
    # CACHE INVALIDATION
    # -----------------------------
    @staticmethod
    def _invalidate_cache(module_id: int):

        try:
            for i in [10, 20, 50, 100]:
                CacheService.delete(f"leaderboard:module:{module_id}:{i}")
                CacheService.delete(f"leaderboard:global:{i}")

        except Exception:
            logger.warning("Cache invalidation failed")

    # -----------------------------
    # GLOBAL LEADERBOARD
    # -----------------------------
    @staticmethod
    def get_global_rankings(
        db: Session,
        limit: int = 10
    ) -> List[Dict]:

        limit = min(limit, 100)
        cache_key = f"leaderboard:global:{limit}"

        cached = CacheService.get_json(cache_key)
        if cached:
            return cached

        results = (
            db.query(
                User.username.label("username"),
                UserProgression.total_xp.label("total_xp"),
                UserProgression.level.label("level")
            )
            .join(UserProgression, User.id == UserProgression.user_id)
            .order_by(UserProgression.total_xp.desc())
            .limit(limit)
            .all()
        )

        rankings = [
            {
                "username": r.username,
                "total_xp": int(r.total_xp),
                "level": int(r.level),
                "rank": idx + 1
            }
            for idx, r in enumerate(results)
        ]

        CacheService.set_json(cache_key, rankings, ex=300)

        return rankings

    # -----------------------------
    # MODULE LEADERBOARD
    # -----------------------------
    @staticmethod
    def get_module_rankings(
        db: Session,
        module_id: int,
        limit: int = 10
    ) -> List[Dict]:

        limit = min(limit, 100)
        cache_key = f"leaderboard:module:{module_id}:{limit}"

        cached = CacheService.get_json(cache_key)
        if cached:
            return cached

        results = leaderboard_repository.get_top_scores_for_module(
            db, module_id=module_id, limit=limit
        )

        rankings = [
            {
                "username": r.username,  
                "top_score": int(r.top_score),
                "rank": idx + 1
            }
            for idx, r in enumerate(results)
        ]

        CacheService.set_json(cache_key, rankings, ex=120)

        return rankings


# -----------------------------
# FASTAPI DEPENDENCY WRAPPER
# -----------------------------
def get_leaderboard_service():
    return LeaderboardService