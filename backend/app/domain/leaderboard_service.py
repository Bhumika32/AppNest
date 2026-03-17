from typing import Optional
from sqlalchemy.orm import Session
from app.models.leaderboard import Leaderboard
from datetime import datetime

class LeaderboardService:
    """
    Handles leaderboard score updates and rank retrieval.
    """

    @staticmethod
    def update_score(
        db: Session, user_id: int, module_key: str, score: int) -> Optional[Leaderboard]:
        """
        Updates a user's top score for a specific module.
        Recalculates rank (simplified for now).
        """
        # 1. Get existing entry
        entry = db.query(Leaderboard).filter_by(user_id=user_id, module_key=module_key).first()

        if not entry:
            entry = Leaderboard(user_id=user_id, module_key=module_key, top_score=score)
            db.add(entry)
        elif score > entry.top_score:
            entry.top_score = score
            entry.last_updated = datetime.utcnow()
        
        db.flush()
        
        # 2. Recalculate ranks for this module (simplified for MVP)
        # In production, this might be a background task or sorted on read
        LeaderboardService._update_ranks(db, module_key)
        
        return entry

    @staticmethod
    def _update_ranks(
        db: Session, module_key: str):
        """
        Updates the rank column for all users in a specific module.
        """
        entries = db.query(Leaderboard).filter_by(module_key=module_key).order_by(Leaderboard.top_score.desc()).all()
        for i, entry in enumerate(entries):
            entry.rank = i + 1
        db.flush()

    @staticmethod
    def get_global_rankings(
        db: Session, limit: int = 10):
        """
        Retrieves global top scores across all modules with Redis caching.
        """
        from app.core.redis_client import neural_cache
        from app.models.user_progression import UserProgression
        from app.models.user import User
        
        cache_key = f"leaderboard:global:{limit}"
        cached_data = neural_cache.get(cache_key)
        if cached_data:
            return cached_data
            
        results = db.query(User.username, UserProgression.total_xp, UserProgression.level) \
            .join(UserProgression, User.id == UserProgression.user_id) \
            .order_by(UserProgression.total_xp.desc()) \
            .limit(limit).all()
            
        rankings = [
            {"name": r[0], "xp": r[1], "level": r[2], "rank": i + 1}
            for i, r in enumerate(results)
        ]
        
        # Cache for 5 minutes
        neural_cache.set(cache_key, rankings, ex=300)
        
        return rankings

    @staticmethod
    def _invalidate_cache():
        """Invalidates all leaderboard caches."""
        from app.core.redis_client import neural_cache
        # Simple invalidation strategy (can be refined to specific keys)
        # In this context, we just wait for expiry or manually clear known keys
        neural_cache.set("leaderboard:global:10", None) # Clear default
