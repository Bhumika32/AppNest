# File: app/domain/lifecycle_service.py

import logging
from sqlalchemy.orm import Session

from app.models.game_session import GameSession
from app.platform.module_registry import get_executor

from app.services.module_service import ModuleService
from app.services.leaderboard_service import LeaderboardService

from app.domain.xp_domain import XPDomain
from app.domain.event_bus import EventBus
from app.domain.experience_engine import ExperienceEngine

from app.core.cache_service import CacheService

logger = logging.getLogger(__name__)


class LifecycleService:

    @staticmethod
    def execute_module(db: Session, user_id: int, slug: str, payload: dict, entry_id=None):

        module = ModuleService.get_module_by_slug(db, slug)

        if not module:
            raise ValueError("Module not found")

        # -----------------------------
        # COOLDOWN
        # -----------------------------
        cooldown_key = f"cooldown:{user_id}:{slug}"

        if CacheService.get_json(cooldown_key):
            raise ValueError("Cooldown active")

        CacheService.set_json(cooldown_key, True, ex=2)

        # -----------------------------
        # EXECUTION
        # -----------------------------
        executor = get_executor(module.module_id)

        result = executor.safe_execute(payload, user_id)

        if not result.get("completed"):
            return result

        return LifecycleService._complete(
            db, user_id, module, result, payload, entry_id
        )

    @staticmethod
    def _complete(db, user_id, module, result, payload, entry_id):

        unique_hash = f"{user_id}:{module.module_id}:{entry_id or result.get('score')}"

        with db.begin():

            # SESSION
            session = GameSession(
                user_id=user_id,
                module_id=module.module_id,
                score=result.get("score", 0),
                duration_seconds=payload.get("duration", 0),
            )
            db.add(session)

            # -----------------------------
            # XP
            # -----------------------------
            if module.type == "game":
                base_xp = XPDomain.calculate_game_xp(
                    score=result.get("score", 0),
                    difficulty=payload.get("difficulty", "easy")
                )
            else:
                base_xp = XPDomain.calculate_tool_xp(
                    is_first_use=True,
                    is_repeat=False
                )

            xp_res = XPDomain.award_xp(   # ⚠️ assuming static, fix if not
                db=db,
                user_id=user_id,
                module_id = module.module_id,
                base_xp=base_xp,
                unique_hash=unique_hash
            )

            # -----------------------------
            # LEADERBOARD
            # -----------------------------
            LeaderboardService.update_score(
                db, user_id, module.module_id, result.get("score", 0)
            )

        # -----------------------------
        # EVENTS
        # -----------------------------
        EventBus.publish("XP_GRANTED", {
            "user_id": user_id,
            "xp": xp_res
        })

        # -----------------------------
        # EXPERIENCE ENGINE
        # -----------------------------
        ExperienceEngine.process_module_result(
            db,
            user_id,
            module.module_id,
            {
                "score": result.get("score", 0),
                "completed": True,
                "lifecycle_res": xp_res
            }
        )

        return {
            "xp": xp_res
        }