"""
File: app/repositories/leaderboard_repository.py

Handles database operations related to leaderboard data.

Design principles:
- Always return structured query results (no raw tuples)
- Use explicit labels to prevent positional bugs
- Keep repository strictly focused on data access (no business logic)
"""

from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.leaderboard import Leaderboard
from app.models.user import User
from app.repositories.base_repository import BaseRepository


class LeaderboardRepository(BaseRepository[Leaderboard]):
    """
    Repository for leaderboard-related database operations.
    """

    def __init__(self):
        super().__init__(Leaderboard)

    # -----------------------------
    # LOCKED FETCH (FOR SCORE UPDATE)
    # -----------------------------
    def get_user_score_for_update(
        self,
        db: Session,
        user_id: int,
        module_id: int
    ) -> Optional[Leaderboard]:
        """
        Fetch a user's leaderboard entry for a specific module
        with row-level locking (FOR UPDATE).

        Used during score updates to prevent race conditions.
        """
        return (
            db.query(self.model)
            .filter(
                self.model.user_id == user_id,
                self.model.module_id == module_id,
            )
            .with_for_update()
            .first()
        )

    # -----------------------------
    # MODULE LEADERBOARD
    # -----------------------------
    def get_top_scores_for_module(
        self,
        db: Session,
        module_id: int,
        limit: int = 10
    ) -> List:
        """
        Fetch top scores for a given module.

        Returns:
            List of rows with named attributes:
            - username (str)
            - top_score (int)

        IMPORTANT:
        We use labels to ensure attribute-based access instead of tuple indexing.
        """
        return (
            db.query(
                User.username.label("username"),
                self.model.top_score.label("top_score")
            )
            .join(User, User.id == self.model.user_id)
            .filter(self.model.module_id == module_id)
            .order_by(self.model.top_score.desc())
            .limit(limit)
            .all()
        )


# Singleton instance (used across services)
leaderboard_repository = LeaderboardRepository()

# from typing import Optional, List
# from sqlalchemy.orm import Session
# from app.models.leaderboard import Leaderboard
# from app.models.user import User
# from app.repositories.base_repository import BaseRepository

# class LeaderboardRepository(BaseRepository[Leaderboard]):
#     def __init__(self):
#         super().__init__(Leaderboard)

#     def get_user_score_for_update(self, db: Session, user_id: int, module_key: str) -> Optional[Leaderboard]:
#         return db.query(self.model).filter(
#             self.model.user_id == user_id,
#             self.model.module_key == module_key
#         ).with_for_update().first()

#     def get_top_scores_for_module(self, db: Session, module_key: str, limit: int = 10) -> List[tuple]:
#         return db.query(User.username, self.model.top_score).join(
#             User, User.id == self.model.user_id
#         ).filter(
#             self.model.module_key == module_key
#         ).order_by(
#             self.model.top_score.desc()
#         ).limit(limit).all()

# leaderboard_repository = LeaderboardRepository()
