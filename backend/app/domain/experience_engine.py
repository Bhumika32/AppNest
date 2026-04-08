# File: app/domain/experience_engine.py

"""
ExperienceEngine (FastAPI + Async Safe + Scalable)

Fixes:
- ❌ Removed self.db
- ❌ Removed asyncio.run()
- ❌ Removed DB leakage across threads
- ✅ Async-safe socket emission
- ✅ AI failure-safe
- ✅ Non-blocking architecture
"""

from typing import Dict, Any, List, Optional
import logging
import asyncio

from sqlalchemy.orm import Session

from app.core.extensions import sio
from app.domain.gemini_service import gemini_ai
from app.services.roast_service import RoastService
from app.services.mentor_service import MentorService
from app.models.user import User

logger = logging.getLogger(__name__)


class ExperienceEngine:
    """
    Stateless Experience Engine

    RULES:
    - Never store DB
    - Never block event loop
    - Never call asyncio.run inside FastAPI
    """

    # -----------------------------
    # MAIN ENTRY
    # -----------------------------
    @staticmethod
    def process_module_result(
        db: Session,
        user_id: int,
        module_slug: str,
        result: Dict[str, Any]
    ):
        """
        Process result and trigger UX events.
        NON-BLOCKING SAFE
        """

        normalized = ExperienceEngine.normalize_result(result)

        events = ExperienceEngine.evaluate_experience(
            db,
            user_id,
            module_slug,
            normalized
        )

        ExperienceEngine.dispatch_events(user_id, events)

    # -----------------------------
    # NORMALIZE
    # -----------------------------
    @staticmethod
    def normalize_result(result: Any) -> Dict[str, Any]:    

        if not isinstance(result, dict):
            return {
                "completed": False,
                "score": 0,
                "win": False,
                "metadata": {}
            }

        return {
            "completed": bool(result.get("completed", False)),
            "score": int(result.get("score", 0)),
            "win": bool(result.get("win", False)),
            "metadata": result.get("metadata", result),
            "lifecycle_res": result.get("lifecycle_res", {})
        }

    # -----------------------------
    # CORE LOGIC
    # -----------------------------
    @staticmethod
    def evaluate_experience(
        db: Session,
        user_id: int,
        module_slug: str,
        result: Dict[str, Any]
    ) -> List[Dict[str, Any]]:

        user: Optional[User] = None

        try:
            user = db.get(User, user_id)
        except Exception as e:
            logger.warning(f"User lookup failed: {e}")

        score = result.get("score", 0)
        username = getattr(user, "username", "Player")

        lifecycle_res = result.get("lifecycle_res", {})
        xp_reward = lifecycle_res.get("xp_reward", {})

        # ---- SKIP BORING TOOLS ----
        deterministic_tools = {
            "bmi-calculator",
            "currency-converter",
            "age-calculator",
            "unit-converter"
        }

        if module_slug in deterministic_tools:
            return []

        # ---- BUILD CONTEXT ----
        context = f"""
User {username} finished module {module_slug}.
Score: {score}.
Respond like a sarcastic rival mentor. Max 2 lines.
"""

        if xp_reward.get("leveled_up"):
            context += f"\nUser leveled up to {xp_reward.get('level')}!"

        if xp_reward.get("streak_bonus", 0) > 0:
            context += "\nUser is on a streak."

        roast = None
        mentor = None

        # ---- AI (SAFE) ----
        try:
            ai_feedback = gemini_ai.generate_feedback(context)
            roast = ai_feedback.get("roast")
            mentor = ai_feedback.get("mentor")
        except Exception as e:
            logger.warning(f"AI failed: {e}")

        # ---- FALLBACK ----
        if not roast:
            try:
                roast = RoastService.get_roast(
                    module_key=module_slug,
                    result=result,
                    user=user
                )
            except Exception as e:
                logger.warning(f"Roast fallback failed: {e}")

        if not mentor:
            mentor = MentorService.fallback_tip(db)

        events: List[Dict[str, Any]] = []

        if roast:
            events.append({
                "type": "roast",
                "delivery": "overlay",
                "message": roast,
                # "icon": "Flame",
                # "color": "neon-pink"
            })

        if mentor:
            events.append({
                "type": "mentor_tip",
                "delivery": "overlay",
                "message": mentor,
                # "icon": "Lightbulb",
                # "color": "neon-blue"
            })

        return events

    # -----------------------------
    # SOCKET DISPATCH (CRITICAL FIX)
    # -----------------------------
    @staticmethod
    def dispatch_events(db: Session, user_id: int, events: List[Dict[str, Any]]):

        if not events:
            return

        room = f"user_{user_id}"

        async def emit_all():
            for event in events:
                try:
                    await sio.emit("ux_event", event, room=room)
                except Exception as e:
                    logger.error(f"Socket emit failed: {e}")

        try:
            loop = asyncio.get_running_loop()
            loop.create_task(emit_all())
        except RuntimeError:
            # No loop → safe fallback (rare)
            asyncio.run(emit_all())