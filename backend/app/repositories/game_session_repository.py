# File: app/repositories/game_session_repository.py

from typing import List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import func, case

from app.models.game_session import GameSession
from app.models.module import Module
from app.repositories.base_repository import BaseRepository


class GameSessionRepository(BaseRepository[GameSession]):
    """
    Repository for game session analytics and queries.
    """

    def __init__(self):
        super().__init__(GameSession)

    # -----------------------------
    # RECENT SESSIONS
    # -----------------------------
    def get_recent_sessions(
        self,
        db: Session,
        user_id: int,
        limit: int = 10
    ) -> List[GameSession]:
        return (
            db.query(self.model)
            .filter(self.model.user_id == user_id)
            .order_by(self.model.created_at.desc())
            .limit(limit)
            .all()
        )

    # -----------------------------
    # COUNT BY MODULE TYPE
    # -----------------------------
    def get_counts_by_module_type(
        self,
        db: Session,
        user_id: int
    ) -> Tuple[int, int]:
        """
        Returns:
            (games_played, tools_used)
        """

        result = (
            db.query(
                func.sum(
                    case((Module.type == "game", 1), else_=0)
                ).label("games_played"),

                func.sum(
                    case((Module.type == "tool", 1), else_=0)
                ).label("tools_used"),
            )
            .join(self.model.module)  # ✅ FIXED JOIN
            .filter(self.model.user_id == user_id)
            .first()
        )

        if not result:
            return 0, 0

        return (
            int(result.games_played or 0),
            int(result.tools_used or 0),
        )


# Singleton
game_session_repository = GameSessionRepository()

# from typing import List, Tuple
# from sqlalchemy.orm import Session
# from sqlalchemy import  func
# from sqlalchemy import  case
# from app.models.game_session import GameSession
# from app.models.module import Module
# from app.repositories.base_repository import BaseRepository

# class GameSessionRepository(BaseRepository[GameSession]):
#     def __init__(self):
#         super().__init__(GameSession)

#     def get_recent_sessions(self, db: Session, user_id: int, limit: int = 10) -> List[GameSession]:
#         return db.query(self.model).filter(
#             self.model.user_id == user_id
#         ).order_by(self.model.created_at.desc()).limit(limit).all()

#     def get_counts_by_module_type(self, db: Session, user_id: int) -> Tuple[int, int]:
#         counts = db.query(
#             func.sum(case((Module.type == "game", 1), else_=0)),
#             func.sum(case((Module.type == "tool", 1), else_=0))
#         ).join(Module, self.model.game_key == Module.slug).filter(
#             self.model.user_id == user_id
#         ).first()
        
#         return counts[0] or 0, counts[1] or 0

# game_session_repository = GameSessionRepository()
