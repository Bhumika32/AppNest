# app/services/module_service.py

from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
import logging

from app.repositories.module_repository import ModuleRepository
from app.repositories.analytics_repository import AnalyticsRepository
from app.repositories.progression_repository import ProgressionRepository
from app.repositories.xp_transaction_repository import XPTransactionRepository

from app.services.progression_service import ProgressionService
from app.services.leaderboard_service import LeaderboardService
from app.services.roast_service import RoastService
from app.services.mentor_service import MentorService

from app.platform.module_registry import get_executor
from app.models.game_session import GameSession
from app.domain.xp_domain import XPDomain
from app.core.cache_service import CacheService

from app.domain.event_bus import EventBus, Events

logger = logging.getLogger(__name__)


class ModuleService:

    # -----------------------------
    # FETCH MODULES
    # -----------------------------
    @staticmethod
    def get_all_modules(db: Session, type_filter: Optional[str]):
        return ModuleRepository().get_all_active(db, type_filter)

    @staticmethod
    def get_module_by_slug(db: Session, slug: str):
        return ModuleRepository().get_active_by_slug(db, slug)

    # -----------------------------
    # ANALYTICS
    # -----------------------------
    @staticmethod
    def track_start(db: Session, user_id: int, module_id: int):

        lock_key = f"app:session:{user_id}:{module_id}"

        if CacheService.get_json(lock_key):
            logger.warning(f"[DUPLICATE_SESSION] user={user_id}, module={module_id}")

        entry = AnalyticsRepository().create(db, {
            "user_id": user_id,
            "module_id": module_id,
            "event_type": "start"
        })

        CacheService.set_json(lock_key, entry.id, ex=3600)

        db.commit()

        return entry.id

    @staticmethod
    def track_end(db: Session, user_id: int, entry_id: int, duration: int):

        entry = AnalyticsRepository().get_by_id(db, entry_id)

        if not entry:
            raise ValueError("Session not found")

        if entry.user_id != user_id:
            raise ValueError("Unauthorized")

        AnalyticsRepository().update(db, entry, {
            "event_type": "end",
            "duration": duration
        })

        CacheService.delete(f"app:session:{user_id}:{entry.module_id}")

        db.commit()

        return True

    # -----------------------------
    # EXECUTION PIPELINE
    # -----------------------------
    @staticmethod
    def execute_module(db: Session, user_id: int, slug: str, payload: dict, entry_id: Optional[int] = None):

        module = ModuleService.get_module_by_slug(db, slug)

        if not module:
            raise ValueError(f"Module not found: {slug}")

        cooldown_key = f"cooldown:{user_id}:{slug}"

        if CacheService.get_json(cooldown_key):
            raise ValueError("Cooldown active. Please wait.")

        CacheService.set_json(cooldown_key, True, ex=1)

        executor = get_executor(module.component_key)

        result = executor.safe_execute(
            payload,
            type('obj', (object,), {'id': user_id, 'username': 'User'})()
        )

        if not result.get("completed"):
            return {
                "success": True,
                "status": result.get("status", "ongoing"),
                "data": result.get("data", {}),
                "completed": False
            }

        return ModuleService._finalize_execution(
            db,
            user_id,
            module,
            result,
            payload,
            entry_id
        )

    # -----------------------------
    # FINALIZATION PIPELINE
    # -----------------------------
    @staticmethod
    def _finalize_execution(db: Session, user_id: int, module, result: Dict, payload: Dict, entry_id: Optional[int]):

        unique_hash = f"{user_id}:{module.component_key}:{entry_id or result.get('score', 0)}:{payload.get('timestamp', 0)}"

        try:

            session = GameSession(
                user_id=user_id,
                module_id=module.id,
                score=result.get("score", 0),
                duration_seconds=payload.get("duration", 0),
            )

            db.add(session)

            # XP calculation
            if module.type == "game":

                status = str(result.get("status", "win")).lower()

                outcome = "win" if "win" in status else \
                          "draw" if "draw" in status else "loss"

                base_xp = XPDomain.calculate_game_xp(
                    #result=outcome,
                    difficulty=payload.get("difficulty", "easy"),
                    score=result.get("score", 0)
                )

            else:

                base_xp = XPDomain.calculate_tool_xp(
                    is_first_use=True,
                    is_repeat=False
                )

            prog_service = ProgressionService(
                progression_repo=ProgressionRepository(),
                xp_repo=XPTransactionRepository()
            )

            xp_res = prog_service.award_xp(
                db=db,
                user_id=user_id,
                module_id=module.id,
                base_xp=base_xp,
                unique_hash=unique_hash
            )

            LeaderboardService.update_score(
                db,
                user_id,
                module.id,
                result.get("score", 0)
            )

            db.commit()

        except Exception as e:
            db.rollback()
            logger.error(f"Error finalizing execution: {e}")
            raise

        # -----------------------------
        # EVENT EMISSION
        # -----------------------------
        if xp_res.get("status") == "success":

            EventBus.publish(
                Events.XP_GRANTED,
                {
                    "db": db,
                    "user_id": user_id,
                    "xp_awarded": xp_res.get("xp_awarded"),
                    "module_name": module.component_key
                }
            )

            if xp_res.get("leveled_up"):

                EventBus.publish(
                    Events.LEVEL_UP,
                    {
                        "db": db,
                        "user_id": user_id,
                        "level": xp_res.get("level")
                    }
                )

        roast = RoastService.get_roast(module.component_key, result)

        advice = MentorService.get_advice(
            db,
            module.component_key,
            result
        )

        return {
            "success": True,
            "status": result.get("status", "completed"),
            "data": result.get("data", {}),
            "completed": True,
            "lifecycle": {
                "xp_reward": xp_res
            },
            "roast": roast,
            "advice": advice
        }


def get_module_service():
    return ModuleService

    # def execute_module(
    #     db: Session,
    #     user_id: int,
    #     slug: str,
    #     payload: dict,
    #     entry_id: Optional[int] = None
    # ):
    #     """
    #     CLEAN ARCHITECTURE:
    #     - Stateless gameplay allowed
    #     - Session required ONLY on completion
    #     """

    #     module = ModuleService.get_module_by_slug(db, slug)
    #     if not module:
    #         raise ValueError(f"Module not found: {slug}")

    #     # -----------------------------
    #     # 1. COOLDOWN (short!)
    #     # -----------------------------
    #     cooldown_key = f"cooldown:{user_id}:{slug}"
    #     if CacheService.get_json(cooldown_key):
    #         raise ValueError("Too fast. Slow down.")
    #     CacheService.set_json(cooldown_key, True, ex=1)

    #     # -----------------------------
    #     # 2. EXECUTE MODULE (STATELESS)
    #     # -----------------------------
    #     executor = get_executor(module.component_key)

    #     result = executor.safe_execute(
    #         payload,
    #         type('obj', (object,), {'id': user_id})()
    #     )

    #     # -----------------------------
    #     # ✅ KEY FIX: ALLOW STATELESS TURNS
    #     # -----------------------------
    #     if not result.get("completed"):
    #         return {
    #             "success": True,
    #             "status": result.get("status", "ongoing"),
    #             "data": result.get("data", {}),
    #             "completed": False
    #         }

    #     # -----------------------------
    #     # ✅ ONLY COMPLETION NEEDS SESSION
    #     # -----------------------------
    #     if not entry_id:
    #         raise ValueError("entry_id required for completion")

    #     return ModuleService._finalize_execution(
    #         db, user_id, module, result, payload, entry_id
    #     )

    # # -----------------------------
    # # FINALIZATION (UNCHANGED)
    # # -----------------------------
    # @staticmethod
    # def _finalize_execution(db: Session, user_id: int, module, result: Dict, payload: Dict, entry_id: Optional[int]):

    #     unique_hash = f"{user_id}:{module.component_key}:{entry_id}:{payload.get('timestamp', 0)}"

    #     try:
    #         session = GameSession(
    #             user_id=user_id,
    #             game_key=module.component_key,
    #             score=result.get("score", 0),
    #             duration_seconds=payload.get("duration", 0),
    #         )
    #         db.add(session)

    #         if module.type == "game":
    #             status = str(result.get("status", "win")).lower()
    #             outcome = "win" if "win" in status else "draw" if "draw" in status else "loss"

    #             base_xp = XPDomain.calculate_game_xp(
    #                 result=outcome,
    #                 difficulty=payload.get("difficulty", "easy"),
    #                 score=result.get("score", 0)
    #             )
    #         else:
    #             base_xp = XPDomain.calculate_tool_xp(
    #                 is_first_use=True,
    #                 is_repeat=False
    #             )

    #         prog_service = ProgressionService(
    #             progression_repo=ProgressionRepository(),
    #             xp_repo=XPTransactionRepository()
    #         )

    #         xp_res = prog_service.award_xp(
    #             db=db,
    #             user_id=user_id,
    #             module_key=module.component_key,
    #             base_xp=base_xp,
    #             unique_hash=unique_hash
    #         )

    #         LeaderboardService.update_score(
    #             db, user_id, module.component_key, result.get("score", 0)
    #         )

    #         db.commit()

    #     except Exception as e:
    #         db.rollback()
    #         logger.error(f"Error finalizing execution: {e}")
    #         raise

    #     roast = RoastService.get_roast(module.component_key, result)
    #     advice = MentorService.get_advice(db, module.component_key, result)

    #     return {
    #         "success": True,
    #         "status": result.get("status", "completed"),
    #         "data": result.get("data", {}),
    #         "completed": True,
    #         "lifecycle": {
    #             "xp_reward": xp_res,
    #         },
    #         "roast": roast,
    #         "advice": advice
    #     }

    