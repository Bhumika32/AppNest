from app.core.extensions import db
from app.models.game_session import GameSession
from app.services.progression_service import ProgressionService
from app.services.module_service import ModuleService
from app.services.event_bus import EventBus, Events
from app.platform.module_registry import get_executor
from datetime import datetime

class LifecycleService:
    """
    Manages the lifecycle of modules (START -> ACTIVE -> COMPLETE -> REWARD).
    """

    @staticmethod
    def execute_module(user_id: int, module_slug: str, payload: dict, entry_id: int = None) -> dict:
        """
        Executes a module via the platform executor and processes lifecycle.
        """
        from app.models.user import User
        user = User.query.get(user_id)
        # 1. Resolve Module from slug
        module = ModuleService.get_module_by_slug(module_slug)
        if not module:
             raise ValueError(f"Module not found: {module_slug}")

        # 2. Execute module logic via platform layer
        try:
            executor = get_executor(module_slug)
            result = getattr(executor, 'safe_execute', executor.execute)(payload, user)
        except Exception:
            import traceback
            traceback.print_exc()
            result = {
                "error": "MODULE_EXECUTION_FAILED",
                "message": "Tool execution failed"
            }
        
        # 3. Process lifecycle completion
        # Determine if execution constitutes completion
        # Tools always complete. Games complete if they flag it.
        is_complete = True
        if module.type == "game":

            if not isinstance(result, dict):
                is_complete = False

            else:
                status = result.get("status")

                is_complete = (
                    result.get("is_complete", False)
                    or result.get("win", False)
                    or result.get("is_over", False)
                    or status in ["player_win", "ai_win", "draw", "completed"]
                )
                
        lifecycle_res = None
        if is_complete:
            completion_payload = {
                'module_id': module.id,
                'module_slug': module_slug,
                'score': result.get('score', 0) if isinstance(result, dict) else 0,
                'duration': payload.get('duration', 0),
                'difficulty': payload.get('difficulty', 'EASY'),
                'result': result.get('status', 'completed') if isinstance(result, dict) else 'completed',
                'metadata': result,
                'entry_id': entry_id
            }
            lifecycle_res = LifecycleService.complete_module(user_id, completion_payload)

        return {
            "executor_result": result, 
            "lifecycle": lifecycle_res,
            "module": module.to_dict(),
            "is_complete": is_complete
        }

    @staticmethod
    def complete_module(user_id: int, payload: dict) -> dict:
        """
        Processes a module completion, awards XP, and fires events.
        payload expects: module_id, score, duration, difficulty, result, metadata
        """
        import json
        module_id = payload.get('module_id')
        module_slug = payload.get('module_slug', 'unknown')
        score = payload.get('score', 0)
        duration = payload.get('duration', 0)
        difficulty = payload.get('difficulty', 'EASY')
        result_status = payload.get('result', 'completed')
        metadata = payload.get('metadata', {})

        # Ensure metadata contains result_status since status column doesn't exist
        if isinstance(metadata, dict):
            metadata['status'] = result_status

        # 1. Close out any Game Session / record it
        session = GameSession(
            user_id=user_id,
            game_key=module_slug,
            score=score,
            duration_seconds=duration,
            meta=json.dumps(metadata) if isinstance(metadata, dict) else str(metadata)
        )
        db.session.add(session)

        # 2. Get Module to determine base XP
        from app.models.module import Module
        module = Module.query.get(module_id)
        base_xp = module.xp_reward_base if module else 10

        # 3. Reward XP
        # In a real scenario, we might calculate performance_bonus from score
        performance_bonus = int(score / 100) if score > 0 else 0
        
        xp_result = ProgressionService.award_xp(
            user_id=user_id,
            module_id=module_id,
            base_reward=base_xp,
            difficulty=difficulty,
            performance_bonus=performance_bonus,
            reason=f"Completed {module.name if module else 'Module'}"
        )

        db.session.commit()

        # 4. Fire Events
        EventBus.publish(Events.MODULE_COMPLETED, {
            "user_id": user_id,
            "module_id": module_id,
            "session_id": session.id,
            "result": result_status,
            "score": score
        })

        EventBus.publish(Events.XP_GRANTED, {
            "user_id": user_id,
            "xp_awarded": xp_result["xp_awarded"],
            "new_total": xp_result["new_total"]
        })

        if xp_result.get("leveled_up"):
            EventBus.publish(Events.LEVEL_UP, {
                "user_id": user_id,
                "new_level": xp_result["level"],
                "rank_title": xp_result["rank_title"]
            })

        return {
            "status": "success",
            "xp_reward": xp_result,
            "session_id": session.id
        }
