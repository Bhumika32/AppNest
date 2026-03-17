# File: backend/app/domain/lifecycle_service.py
# -----------------------------------------------------------------------------
# Central lifecycle manager for module execution in the AppNest platform.
#
# Responsibilities:
# - Execute module logic
# - Normalize results
# - Record gameplay sessions
# - Award XP
# - Update leaderboard
# - Process quests
# - Emit platform events
#
# Architecture Rules:
# - ExperienceEngine handles ONLY AI roast + mentor + UI overlays
# - Persistent notifications are created via EventBus -> notification_handlers
# -----------------------------------------------------------------------------

import json

from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.game_session import GameSession
from app.models.module import Module
from app.models.user import User

from app.domain.progression_service import ProgressionService
from app.domain.module_service import ModuleService
from app.domain.event_bus import EventBus, Events
from app.domain.experience_engine import ExperienceEngine
from app.domain.leaderboard_service import LeaderboardService
from app.domain.quest_service import QuestService

from app.platform.module_registry import get_executor
from app.platform.module_result import ModuleResult


class LifecycleService:

    # -------------------------------------------------------------------------
    # MODULE EXECUTION
    # -------------------------------------------------------------------------
    @staticmethod
    def execute_module(

        db: Session, 
        user_id: int, 
        module_slug: str, 
        payload: dict, 
        entry_id: int = None):

        user = db.get(User, user_id)
        module = ModuleService.get_module_by_slug(db, module_slug)

        if not module:
            raise ValueError(f"Module not found: {module_slug}")

        from app.core.redis_client import neural_cache

        cooldown_amount = 3 if module.type == 'tool' else 1
        cooldown_key = f"cooldown:{user_id}:{module_slug}"
        if neural_cache.get(cooldown_key):
            return {
                "executor_result": {"error": "COOLDOWN_ACTIVE", "message": f"Please wait {cooldown_amount}s before executing again."},
                "lifecycle": None,
                "module": module.to_dict(),
                "is_complete": False
            }
        neural_cache.set(cooldown_key, "1", ex=cooldown_amount)

        if entry_id:
            lock_key = f"session_active:{user_id}:{module.id}"
            active_entry = neural_cache.get(lock_key)
            if active_entry and str(active_entry) != str(entry_id):
                return {
                    "executor_result": {"error": "INVALID_SESSION", "message": "Session has expired or is invalid."},
                    "lifecycle": None,
                    "module": module.to_dict(),
                    "is_complete": False
                }

        try:
            executor = get_executor(module_slug)
            result = getattr(executor, "safe_execute", executor.execute)(payload, user)

        except KeyError as e:
            raise e
        except Exception:
            import traceback
            traceback.print_exc()

            return {
                "executor_result": {
                    "error": "MODULE_EXECUTION_FAILED",
                    "message": "Module execution failed"
                },
                "lifecycle": None,
                "module": module.to_dict(),
                "is_complete": False
            }

        if isinstance(result, ModuleResult):
            result = result.to_dict()

        if not isinstance(result, dict):
            result = {"raw": result}

        normalized_result = ExperienceEngine.normalize_result(result)
        normalized_result.setdefault("completed", True)
        normalized_result.setdefault("score", 0)
        normalized_result.setdefault("metadata", {})

        score = normalized_result.get("score", 0)
        score = max(0, min(score, 100))
        normalized_result["score"] = score

        is_complete = normalized_result.get("completed", False)
        lifecycle_res = None

        if is_complete:
            completion_payload = {
                "module_id": module.id,
                "module_slug": module_slug,
                "score": score,
                "duration": payload.get("duration", 0),
                "difficulty": payload.get("difficulty", "EASY"),
                "result": normalized_result.get("metadata", {}).get("status", "completed"),
                "metadata": normalized_result.get("metadata", {}),
                "entry_id": entry_id,
                "input": payload
            }

            lifecycle_res = LifecycleService.complete_module(
                user_id,
                completion_payload
            )

            # Architecture fix: delegate mentor processing to async background task
            normalized_result['lifecycle_res'] = lifecycle_res
            
            # import asyncio
            # try:
            #     loop = asyncio.get_event_loop()
            #     if loop.is_running():
            #         loop.create_task(asyncio.to_thread(ExperienceEngine.process_module_result, user_id, module_slug, normalized_result))
            #     else:
            #         asyncio.run(asyncio.to_thread(ExperienceEngine.process_module_result, user_id, module_slug, normalized_result))
            # except Exception as e:
            #      # Fallback if no loop
            #      ExperienceEngine.process_module_result(user_id, module_slug, normalized_result)
            import asyncio

            try:
                loop = asyncio.get_running_loop()
                loop.run_in_executor(
                    None,
                    ExperienceEngine.process_module_result,
                    user_id,
                    module_slug,
                    normalized_result
                )
            except RuntimeError:
                ExperienceEngine.process_module_result(
                    user_id,
                    module_slug,
                    normalized_result
                )

        return {
            "executor_result": result,
            "lifecycle": lifecycle_res,
            "module": module.to_dict(),
            "is_complete": is_complete
        }

    # -------------------------------------------------------------------------
    # MODULE COMPLETION HANDLER
    # -------------------------------------------------------------------------
    @staticmethod
    def complete_module(
        db: Session, user_id: int, payload: dict):

        module_id = payload.get("module_id")
        module_slug = payload.get("module_slug", "unknown")
        score = payload.get("score", 0)
        duration = payload.get("duration", 0)
        difficulty = payload.get("difficulty", "EASY")
        result_status = payload.get("result", "completed")
        metadata = payload.get("metadata", {})

        import json
        from app.core.redis_client import neural_cache
        
        # ATOMIC LOCK: Prevent race condition if multiple execute calls hit for same entry/session
        lock_key = f"xp_lock:{user_id}:{module_slug}:{payload.get('entry_id', 'none')}"
        if not neural_cache.set(lock_key, "locked", ex=30, nx=True):
            return {"status": "already_processed", "message": "Module completion already in progress."}

        if isinstance(metadata, dict):
            metadata["status"] = result_status

        session = GameSession(
            user_id=user_id,
            game_key=module_slug,
            score=score,
            duration_seconds=duration,
            meta=json.dumps(metadata) if isinstance(metadata, dict) else str(metadata)
        )

        db.add(session)

        module = db.get(Module, module_id)
        base_xp = module.xp_reward_base if module else 10
        performance_bonus = 0

        # STREAK CALCULATOR
        streak_bonus = 0
        import datetime
        from app.core.redis_client import neural_cache
        today_str = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        streak_key = f"streak:{user_id}"
        last_active_key = f"last_active:{user_id}"
        
        last_active = neural_cache.get(last_active_key)
        streak = int(neural_cache.get(streak_key) or 0)
        
        if last_active != today_str:
            yesterday_str = (datetime.datetime.utcnow() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
            if last_active == yesterday_str:
                streak += 1
            else:
                streak = 1
            
            neural_cache.set(streak_key, streak)
            neural_cache.set(last_active_key, today_str)
            
            if streak == 3: streak_bonus = 5
            elif streak == 7: streak_bonus = 10
            elif streak == 14: streak_bonus = 20
            
            if streak > 1:
                EventBus.publish(Events.STREAK_UPDATED, {
                    "user_id": user_id,
                    "streak": streak
                })

        # TOOL AND GAME XP RULES
        if module:
            if module.type == 'tool':
                import hashlib
                import json
                input_hash = hashlib.sha256(json.dumps(payload.get('input', {})).encode()).hexdigest()
                hash_key = f"tool_hash:{user_id}:{module_slug}:{input_hash}"
                daily_cap_key = f"tool_cap:{user_id}:{today_str}"
                
                daily_xp = int(neural_cache.get(daily_cap_key) or 0)
                if neural_cache.get(hash_key):
                    base_xp = 0  # Identical input used previously
                elif daily_xp >= 20:
                    base_xp = 0  # Reached daily 20 XP cap for tools
                else:
                    base_xp = min(3, 20 - daily_xp) 
                    neural_cache.set(hash_key, "1", ex=86400)
                    neural_cache.set(daily_cap_key, str(daily_xp + base_xp), ex=86400)
            elif module.type == 'game':
                if duration < 5:
                    base_xp = 0
                else:
                    if module_slug == 'tic-tac-toe':
                        if result_status == 'win': base_xp = 40
                        elif result_status == 'draw': base_xp = 20
                        else: base_xp = 5
                    else:
                        # Hungry Snake, Flappy Bird, Brick Breaker
                        base_xp = max(5, int(score * 1.2)) # Score based scaling + multiplier bonus later
                        performance_bonus = int((score / 50.0) * 10) # extra performance incentive

        xp_result = ProgressionService.award_xp(
            user_id=user_id,
            module_id=module_id,
            base_reward=base_xp,
            difficulty=difficulty,
            performance_bonus=performance_bonus,
            streak_bonus=streak_bonus,
            reason=f"Completed {module.name if module else 'Module'}"
        )

        db.commit()

        LeaderboardService.update_score(user_id, module_slug, score)

        completed_quests = QuestService.process_module_completion(
            db,
            user_id,
            module_slug,
            score
        )

        EventBus.publish(Events.MODULE_COMPLETED, {
            "user_id": user_id,
            "module_id": module_id,
            "session_id": session.id,
            "result": result_status,
            "score": score
        })

        ExperienceEngine.dispatch_events(user_id, [
            {
                "type": "xp_awarded",
                "delivery": "toast",
                "data": xp_result
            }
        ])

        EventBus.publish(Events.XP_GRANTED, {
            "user_id": user_id,
            "xp_awarded": xp_result["xp_awarded"],
            "module_slug": module_slug,
            "module_name": module.name if module else "Module"
        })

        if xp_result.get("leveled_up"):

            ExperienceEngine.dispatch_events(user_id, [
                {
                    "type": "level_up",
                    "delivery": "toast",
                    "data": xp_result
                }
            ])

            EventBus.publish(Events.LEVEL_UP, {
                "user_id": user_id,
                "new_level": xp_result["level"]
            })

        return {
            "status": "success",
            "xp_reward": xp_result,
            "session_id": session.id,
            "completed_quests": [uq.to_dict() for uq in completed_quests]
        }
