# -----------------------------------------------------------------------------
# File: backend/app/domain/experience_engine.py
#
# Description:
# Central orchestration engine for user experience feedback in AppNest.
#
# Responsibilities:
# - Normalize module results
# - Generate AI feedback (roast + mentor tip)
# - Dispatch UI overlay events
#
# Architecture Rule:
# Gemini AI is called ONLY here to prevent duplicate API requests.
#
# Stability Improvements:
# - Defensive result normalization
# - Gemini failure fallback
# - Safe SQLAlchemy lookup
# - Safe async socket emission
# -----------------------------------------------------------------------------

from typing import Dict, Any, List
import logging
import asyncio
from sqlalchemy.orm import Session
from app.core.database import get_db
from fastapi import Depends
from app.core.extensions import  sio
from app.domain.gemini_service import gemini_ai
from app.domain.roast_service import RoastService
from app.domain.mentor_service import MentorService
from app.models.user import User
from fastapi import Depends
logger = logging.getLogger(__name__)


class ExperienceEngine:
    """
    Orchestrates user experience feedback events.
    """

    # -------------------------------------------------------------------------
    # MAIN ENTRY POINT
    # -------------------------------------------------------------------------

    @staticmethod
    def process_module_result(db: Session, user_id: int, module_slug: str, result: Dict[str, Any]):

        normalized_result = ExperienceEngine.normalize_result(result)

        events = ExperienceEngine.evaluate_experience(
            db,
            user_id,
            module_slug,
            normalized_result
        )

        ExperienceEngine.dispatch_events(user_id, events)

    # -------------------------------------------------------------------------
    # RESULT NORMALIZATION
    # -------------------------------------------------------------------------

    @staticmethod
    def normalize_result(result: Dict[str, Any]) -> Dict[str, Any]:

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

    # -------------------------------------------------------------------------
    # EXPERIENCE EVALUATION
    # -------------------------------------------------------------------------

    @staticmethod
    def evaluate_experience(
        db: Session,
        user_id: int,
        module_slug: str,
        result: Dict[str, Any]
    ) -> List[Dict[str, Any]]:

        try:
            user = db.get(User, user_id)
        except Exception as e:
            logger.warning(f"User lookup failed: {e}")
            user = None

        score = result.get("score", 0)
        username = getattr(user, "username", "Player")

        context = f"""
User {username} finished module {module_slug}.
Score: {score}.
Act as a sarcastic rival mentor. React to this game result.
Keep it short (1-2 sentences max).
"""

        lifecycle_res = result.get("lifecycle_res", {})
        xp_reward = lifecycle_res.get("xp_reward", {})

        if xp_reward.get("leveled_up"):
            context += f"\nUser just leveled up to {xp_reward.get('level')}!"

        if xp_reward.get("streak_bonus", 0) > 0:
            context += "\nUser is on a daily login streak."

        deterministic_tools = {
            "bmi-calculator",
            "currency-converter",
            "age-calculator",
            "unit-converter"
        }

        if module_slug in deterministic_tools:
            return []

        roast = None
        mentor = None

        try:
            ai_feedback = gemini_ai.generate_feedback(context)
            roast = ai_feedback.get("roast")
            mentor = ai_feedback.get("mentor")
        except Exception as e:
            logger.warning(f"Gemini feedback generation failed: {e}")

        if not roast:
            roast = RoastService.get_roast(
                module_slug=module_slug,
                result=result,
                user=user
            )

        if not mentor:
            mentor = MentorService.fallback_tip()

        events: List[Dict[str, Any]] = []

        if roast:
            events.append({
                "type": "roast",
                "delivery": "overlay",
                "message": roast,
                "icon": "Flame",
                "color": "neon-pink"
            })

        if mentor:
            events.append({
                "type": "mentor_tip",
                "delivery": "overlay",
                "message": mentor,
                "icon": "Lightbulb",
                "color": "neon-blue"
            })

        return events

    # -------------------------------------------------------------------------
    # EVENT DISPATCH
    # -------------------------------------------------------------------------

    @staticmethod
    def dispatch_events(user_id: int, events: List[Dict[str, Any]]):

        if not events:
            return

        room = f"user_{user_id}"

        for event in events:

            try:

                async def emit():
                    await sio.emit("ux_event", event, room=room)

                try:
                    loop = asyncio.get_running_loop()
                    loop.create_task(emit())
                except RuntimeError:
                    asyncio.run(sio.emit("ux_event", event, room=room))

            except Exception as e:
                logger.error(
                    f"Socket emission failed for event {event.get('type')}: {e}"
                )


experience_engine = ExperienceEngine()
# # -----------------------------------------------------------------------------
# # File: backend/app/domain/experience_engine.py
# #
# # Description:
# # Central orchestration engine for user experience feedback in AppNest.
# #
# # Responsibilities:
# # - Normalize module results
# # - Generate AI feedback (roast + mentor tip)
# # - Dispatch UI overlay events
# # - Create persistent notifications
# #
# # Architecture Rule:
# # Gemini AI is called ONLY here to prevent duplicate API requests.
# #
# # Stability Improvements:
# # - Safe JSON parsing
# # - Safe SQLAlchemy usage
# # - Fallback systems for roast and mentor advice
# # - Defensive socket emission
# # -----------------------------------------------------------------------------

# from typing import Dict, Any, List
# import logging

# from app.core.extensions import db, sio
# from app.domain.notification_service import NotificationService
# from app.domain.gemini_service import gemini_ai
# from app.domain.roast_service import RoastService
# from app.domain.mentor_service import MentorService
# from app.models.user import User

# logger = logging.getLogger(__name__)


# class ExperienceEngine:
#     """
#     Orchestrates user experience feedback events.
#     """

#     # -------------------------------------------------------------------------
#     # MAIN ENTRY POINT
#     # -------------------------------------------------------------------------
#     @staticmethod
#     def process_module_result(user_id: int, module_slug: str, result: Dict[str, Any]):

#         normalized_result = ExperienceEngine.normalize_result(result)

#         events = ExperienceEngine.evaluate_experience(
#             user_id,
#             module_slug,
#             normalized_result
#         )

#         ExperienceEngine.dispatch_events(user_id, events)

#     # -------------------------------------------------------------------------
#     # RESULT NORMALIZATION
#     # -------------------------------------------------------------------------
#     @staticmethod
#     def normalize_result(result: Dict[str, Any]) -> Dict[str, Any]:

#         return {
#             "completed": result.get("completed", False),
#             "score": result.get("score", 0),
#             "win": result.get("win", False),
#             "metadata": result.get("metadata", result)
#         }

#     # -------------------------------------------------------------------------
#     # EXPERIENCE EVALUATION
#     # -------------------------------------------------------------------------
#     @staticmethod
#     def evaluate_experience(
#         user_id: int,
#         module_slug: str,
#         result: Dict[str, Any]
#     ) -> List[Dict[str, Any]]:

#         user = db.session.get(User, user_id)

#         score = result.get("score", 0)

#         username = "Player"
#         if user and getattr(user, "username", None):
#             username = user.username

#         context = f"""
# User {username} finished module {module_slug}.
# Score: {score}.
# Act as a sarcastic rival mentor. React to this game result.
# Keep it short (1-2 sentences max).
# """

#         lifecycle_res = result.get('lifecycle_res', {})
#         if lifecycle_res:
#              xp_reward = lifecycle_res.get('xp_reward', {})
             
#              if xp_reward.get('leveled_up'):
#                  context += f"\nUser just leveled up to {xp_reward.get('level')}!"
#                  if xp_reward.get('level') in [10, 25, 50, 100]:
#                      context += f"\nUser hit a MAJOR milestone rank: {xp_reward.get('rank_title')}!"
                     
#              if xp_reward.get('streak_bonus', 0) > 0:
#                  context += f"\nUser is on a daily login streak!"

#         DETERMINISTIC_TOOLS = {"bmi-calculator", "currency-converter", "age-calculator", "unit-converter"}
        
#         if module_slug in DETERMINISTIC_TOOLS:
#             return []

#         # -------------------------------------------------------------
#         # SINGLE GEMINI CALL
#         # -------------------------------------------------------------
#         ai_feedback = gemini_ai.generate_feedback(context)

#         roast = ai_feedback.get("roast")
#         mentor = ai_feedback.get("mentor")

#         # -------------------------------------------------------------
#         # FALLBACKS
#         # -------------------------------------------------------------
#         if not roast:
#             roast = RoastService.get_roast(
#                 module_slug,
#                 result=result,
#                 user=user
#             )

#         if not mentor:
#             mentor = MentorService.fallback_tip()

#         events = []

#         # Roast Overlay
#         if roast:

#             events.append({
#                 "type": "roast",
#                 "delivery": "overlay",
#                 "message": roast,
#                 "icon": "Flame",
#                 "color": "neon-pink"
#             })

#         # Mentor Overlay
#         if mentor:

#             events.append({
#                 "type": "mentor_tip",
#                 "delivery": "overlay",
#                 "message": mentor,
#                 "icon": "Lightbulb",
#                 "color": "neon-blue"
#             })

#         return events

#     # -------------------------------------------------------------------------
#     # EVENT DISPATCH
#     # -------------------------------------------------------------------------

#     @staticmethod
#     def dispatch_events(user_id: int, events: List[Dict[str, Any]]):

#         """
#         Sends UX events to the frontend only.
#         Persistent notifications are handled by EventBus.
#         """

#         for event in events:

#             try:

#                 import asyncio
#                 try:
#                     loop = asyncio.get_event_loop()
#                     if loop.is_running():
#                         loop.create_task(sio.emit("ux_event", event, room=f"user_{user_id}"))
#                     else:
#                         asyncio.run(sio.emit("ux_event", event, room=f"user_{user_id}"))
#                 except RuntimeError:
#                     pass

#             except Exception as e:

#                 logger.error(
#                     f"Socket emission failed for event {event.get('type')}: {e}"
#             )

# experience_engine = ExperienceEngine()
