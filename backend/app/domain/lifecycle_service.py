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

from app.core.extensions import db
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
    def execute_module(user_id: int, module_slug: str, payload: dict, entry_id: int = None):

        user = db.session.get(User, user_id)
        module = ModuleService.get_module_by_slug(module_slug)

        if not module:
            raise ValueError(f"Module not found: {module_slug}")

        try:
            executor = get_executor(module_slug)
            result = getattr(executor, "safe_execute", executor.execute)(payload, user)

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

        score = normalized_result.get("score", 0)
        score = max(0, min(score, 100))
        normalized_result["score"] = score

        is_complete = normalized_result.get("completed", False)
        lifecycle_res = None

        if is_complete:

            ExperienceEngine.process_module_result(
                user_id,
                module_slug,
                normalized_result
            )

            completion_payload = {
                "module_id": module.id,
                "module_slug": module_slug,
                "score": score,
                "duration": payload.get("duration", 0),
                "difficulty": payload.get("difficulty", "EASY"),
                "result": "completed",
                "metadata": normalized_result.get("metadata", {}),
                "entry_id": entry_id
            }

            lifecycle_res = LifecycleService.complete_module(
                user_id,
                completion_payload
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
    def complete_module(user_id: int, payload: dict):

        module_id = payload.get("module_id")
        module_slug = payload.get("module_slug", "unknown")
        score = payload.get("score", 0)
        duration = payload.get("duration", 0)
        difficulty = payload.get("difficulty", "EASY")
        result_status = payload.get("result", "completed")
        metadata = payload.get("metadata", {})

        if isinstance(metadata, dict):
            metadata["status"] = result_status

        session = GameSession(
            user_id=user_id,
            game_key=module_slug,
            score=score,
            duration_seconds=duration,
            meta=json.dumps(metadata) if isinstance(metadata, dict) else str(metadata)
        )

        db.session.add(session)

        module = db.session.get(Module, module_id)
        base_xp = module.xp_reward_base if module else 10

        performance_bonus = int(score / 100)

        xp_result = ProgressionService.award_xp(
            user_id=user_id,
            module_id=module_id,
            base_reward=base_xp,
            difficulty=difficulty,
            performance_bonus=performance_bonus,
            reason=f"Completed {module.name if module else 'Module'}"
        )

        db.session.commit()

        LeaderboardService.update_score(user_id, module_slug, score)

        completed_quests = QuestService.process_module_completion(
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
                "new_level": xp_result["new_level"]
            })

        return {
            "status": "success",
            "xp_reward": xp_result,
            "session_id": session.id,
            "completed_quests": [uq.to_dict() for uq in completed_quests]
        }
# from app.core.extensions import db
# from app.models.game_session import GameSession
# from app.domain.progression_service import ProgressionService
# from app.domain.module_service import ModuleService
# from app.domain.event_bus import EventBus, Events
# from app.platform.module_registry import get_executor
# from app.platform.module_result import ModuleResult
# from app.domain.roast_service import RoastService
# from app.domain.mentor_service import MentorService
# from datetime import datetime

# class LifecycleService:
#     """
#     Manages the lifecycle of modules (START -> ACTIVE -> COMPLETE -> REWARD).
#     """

#     @staticmethod
#     def execute_module(user_id: int, module_slug: str, payload: dict, entry_id: int = None) -> dict:
#         """
#         Executes a module via the platform executor and processes lifecycle.
#         """
#         from app.models.user import User
#         from app.domain.experience_engine import ExperienceEngine
#         user = User.query.get(user_id)
#         # 1. Resolve Module from slug
#         module = ModuleService.get_module_by_slug(module_slug)
#         if not module:
#              raise ValueError(f"Module not found: {module_slug}")

#         # 2. Execute module logic
#         try:
#             executor = get_executor(module_slug)
#             result = getattr(executor, 'safe_execute', executor.execute)(payload, user)
#         except Exception:
#             import traceback
#             traceback.print_exc()
#             result = {
#                 "error": "MODULE_EXECUTION_FAILED",
#                 "message": "Tool execution failed"
#             }
        
#         # 3. Process lifecycle completion
#         # Standard rules:
#         # - Always treat as completed if frontend sends end/analytics (handled in completion logic)
#         # - Fallback to result.get("completed") if present
#         is_complete = result.get("completed", False) if isinstance(result, dict) else False
        
#         # If the result isn't standardized, normalize it
#         normalized_result = ExperienceEngine.normalize_result(result if isinstance(result, dict) else {"raw": result})
        
#         # 4. Delegate Feedback and Completion to ExperienceEngine if complete
#         lifecycle_res = None
#         roast = None
#         advice = None
        
#         if is_complete:
#             # ExperienceEngine handles all UX decisions
#             ExperienceEngine.process_module_result(user_id, module_slug, result if isinstance(result, dict) else {"raw": result})
            
#             # For backward compatibility with existing controllers expecting these in return
#             # We still generate them here or pull them from the engine if needed
#             roast = RoastService.get_roast(module_slug, module_result=None, user=user) # result is managed in engine now
#             advice = MentorService.get_advice(module_slug, module_result=None, user=user)
            
#             completion_payload = {
#                 'module_id': module.id,
#                 'module_slug': module_slug,
#                 'score': normalized_result["score"],
#                 'duration': payload.get('duration', 0),
#                 'difficulty': payload.get('difficulty', 'EASY'),
#                 'result': 'completed',
#                 'metadata': normalized_result["metadata"],
#                 'entry_id': entry_id
#             }
#             lifecycle_res = LifecycleService.complete_module(user_id, completion_payload)

#         return {
#             "executor_result": result, 
#             "lifecycle": lifecycle_res,
#             "module": module.to_dict(),
#             "is_complete": is_complete,
#             "roast": roast,
#             "advice": advice
#         }

#     @staticmethod
#     def complete_module(user_id: int, payload: dict) -> dict:
#         """
#         Processes a module completion, awards XP, and fires events.
#         """
#         import json
#         from app.domain.experience_engine import ExperienceEngine
        
#         module_id = payload.get('module_id')
#         module_slug = payload.get('module_slug', 'unknown')
#         score = payload.get('score', 0)
#         duration = payload.get('duration', 0)
#         difficulty = payload.get('difficulty', 'EASY')
#         result_status = payload.get('result', 'completed')
#         metadata = payload.get('metadata', {})

#         if isinstance(metadata, dict):
#             metadata['status'] = result_status

#         # 1. Close out any Game Session / record it
#         session = GameSession(
#             user_id=user_id,
#             game_key=module_slug,
#             score=score,
#             duration_seconds=duration,
#             meta=json.dumps(metadata) if isinstance(metadata, dict) else str(metadata)
#         )
#         db.session.add(session)

#         # 2. Get Module
#         from app.models.module import Module
#         module = Module.query.get(module_id)
#         base_xp = module.xp_reward_base if module else 10

#         # 3. Reward XP
#         performance_bonus = int(score / 100) if score > 0 else 0
        
#         xp_result = ProgressionService.award_xp(
#             user_id=user_id,
#             module_id=module_id,
#             base_reward=base_xp,
#             difficulty=difficulty,
#             performance_bonus=performance_bonus,
#             reason=f"Completed {module.name if module else 'Module'}"
#         )

#         db.session.commit()

#         # 4. Gamification Updates
#         from app.domain.leaderboard_service import LeaderboardService
#         from app.domain.quest_service import QuestService

#         LeaderboardService.update_score(user_id, module_slug, score)
#         completed_quests = QuestService.process_module_completion(user_id, module_slug, score)

#         # 5. Emit Centralized Experience Events
#         # Instead of multiple direct EventBus calls, ExperienceEngine can be notified here as well
#         # or we keep EventBus for other subsystems but ensure ExperienceEngine is the one emitting Sockets.
        
#         EventBus.publish(Events.MODULE_COMPLETED, {
#             "user_id": user_id,
#             "module_id": module_id,
#             "session_id": session.id,
#             "result": result_status,
#             "score": score
#         })

#         # ExperienceEngine handles XP, Quest, and Level Up
#         # Both as real-time Toasts and persistent Notifications as requested
#         ExperienceEngine.dispatch_events(user_id, [
#             {
#                 "type": "xp_awarded", 
#                 "delivery": "toast", 
#                 "data": xp_result
#             },
#             {
#                 "type": "xp_earned", 
#                 "delivery": "notification", 
#                 "title": "XP Earned", 
#                 "message": f"You gained {xp_result['xp_awarded']} XP for completing {module_slug}.",
#                 "category": "credit"
#             },
#             {
#                 "type": "module_completed", 
#                 "delivery": "notification", 
#                 "title": "Activity Complete", 
#                 "message": f"You've successfully finished {module_slug.title()}.",
#                 "category": "achievement"
#             }
#         ])

#         if xp_result.get("leveled_up"):
#             ExperienceEngine.dispatch_events(user_id, [
#                 {
#                     "type": "level_up", 
#                     "delivery": "toast", 
#                     "data": xp_result
#                 },
#                 {
#                     "type": "level_up_notif", 
#                     "delivery": "notification", 
#                     "title": "Leveled Up!", 
#                     "message": f"Congratulations! You reached Level {xp_result['level']}.",
#                     "category": "achievement"
#                 }
#             ])

#         for uq in completed_quests:
#             ExperienceEngine.dispatch_events(user_id, [
#                 {
#                     "type": "quest_completed", 
#                     "delivery": "notification", 
#                     "title": "Quest Completed!", 
#                     "message": f"You finished '{uq.quest.title}' and earned {uq.quest.xp_reward} XP.",
#                     "category": "achievement"
#                 }
#             ])

#         return {
#             "status": "success",
#             "xp_reward": xp_result,
#             "session_id": session.id,
#             "completed_quests": [uq.to_dict() for uq in completed_quests]
#         }
