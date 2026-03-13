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
# - Create persistent notifications
#
# Architecture Rule:
# Gemini AI is called ONLY here to prevent duplicate API requests.
#
# Stability Improvements:
# - Safe JSON parsing
# - Safe SQLAlchemy usage
# - Fallback systems for roast and mentor advice
# - Defensive socket emission
# -----------------------------------------------------------------------------

from typing import Dict, Any, List
import logging

from app.core.extensions import db, socketio
from app.domain.notification_service import NotificationService
from app.domain.gemini_service import gemini_ai
from app.domain.roast_service import RoastService
from app.domain.mentor_service import MentorService
from app.models.user import User

logger = logging.getLogger(__name__)


class ExperienceEngine:
    """
    Orchestrates user experience feedback events.
    """

    # -------------------------------------------------------------------------
    # MAIN ENTRY POINT
    # -------------------------------------------------------------------------
    @staticmethod
    def process_module_result(user_id: int, module_slug: str, result: Dict[str, Any]):

        normalized_result = ExperienceEngine.normalize_result(result)

        events = ExperienceEngine.evaluate_experience(
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

        return {
            "completed": result.get("completed", False),
            "score": result.get("score", 0),
            "win": result.get("win", False),
            "metadata": result.get("metadata", result)
        }

    # -------------------------------------------------------------------------
    # EXPERIENCE EVALUATION
    # -------------------------------------------------------------------------
    @staticmethod
    def evaluate_experience(
        user_id: int,
        module_slug: str,
        result: Dict[str, Any]
    ) -> List[Dict[str, Any]]:

        user = db.session.get(User, user_id)

        score = result.get("score", 0)

        username = "Player"
        if user and getattr(user, "username", None):
            username = user.username

        context = f"""
User {username} finished module {module_slug}.
Score: {score}.
"""

        # -------------------------------------------------------------
        # SINGLE GEMINI CALL
        # -------------------------------------------------------------
        ai_feedback = gemini_ai.generate_feedback(context)

        roast = ai_feedback.get("roast")
        mentor = ai_feedback.get("mentor")

        # -------------------------------------------------------------
        # FALLBACKS
        # -------------------------------------------------------------
        if not roast:
            roast = RoastService.get_roast(
                module_slug,
                result=result,
                user=user
            )

        if not mentor:
            mentor = MentorService.fallback_tip()

        events = []

        # Roast Overlay
        if roast:

            events.append({
                "type": "roast",
                "delivery": "overlay",
                "message": roast,
                "icon": "Flame",
                "color": "neon-pink"
            })

        # Mentor Overlay
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

        """
        Sends UX events to the frontend only.
        Persistent notifications are handled by EventBus.
        """

        for event in events:

            try:

                socketio.emit(
                    "ux_event",
                    event,
                    room=f"user_{user_id}"
                )

            except Exception as e:

                logger.error(
                    f"Socket emission failed for event {event.get('type')}: {e}"
            )

experience_engine = ExperienceEngine()
# from typing import Dict, Any, List, Optional
# import logging
# from app.core.extensions import db, socketio
# from app.domain.event_bus import EventBus, Events
# from app.domain.notification_service import NotificationService
# from app.domain.progression_service import ProgressionService
# from app.domain.leaderboard_service import LeaderboardService
# from app.domain.quest_service import QuestService

# logger = logging.getLogger(__name__)

# class ExperienceEngine:
#     """
#     Centralized orchestrator for user experience events.
#     Responsibile for XP, notifications, roasts, mentor advice, and socket emissions.
#     """

#     @staticmethod
#     def process_module_result(user_id: int, module_slug: str, result: Dict[str, Any]):
#         """
#         Main entry point after a module finishes execution.
#         """
#         # 1. Standardize Result
#         normalized_result = ExperienceEngine.normalize_result(result)
        
#         # 2. Determine Experience Events
#         events = ExperienceEngine.evaluate_experience(user_id, module_slug, normalized_result)
        
#         # 3. Dispatch Events (Socket, Database, Notification)
#         ExperienceEngine.dispatch_events(user_id, events)

#     @staticmethod
#     def normalize_result(result: Dict[str, Any]) -> Dict[str, Any]:
#         """
#         Ensures the result follows the target structure.
#         """
#         return {
#             "completed": result.get("completed", True), # Assume completed if reached here
#             "score": result.get("score", 0),
#             "win": result.get("win", False),
#             "metadata": result.get("metadata", result)
#         }

#     @staticmethod
#     def evaluate_experience(user_id: int, module_slug: str, result: Dict[str, Any]) -> List[Dict[str, Any]]:
#         """
#         Logic to decide which feedback should occur.
#         """
#         from app.domain.roast_service import RoastService
#         from app.domain.mentor_service import MentorService
#         from app.models.user import User
        
#         user = User.query.get(user_id)
#         events = []
#         is_win = result.get("win", False)
#         score = result.get("score", 0)
        
#         # 1. Roast (Overlay Only)
#         roast = RoastService.get_roast(module_slug, result=None, user=user)
#         if roast:
#             events.append({
#                 "type": "roast",
#                 "delivery": "overlay",
#                 "message": roast,
#                 "icon": "Flame",
#                 "color": "neon-pink"
#             })
        
#         # 2. Mentor Tip (Overlay Only)
#         advice = MentorService.get_advice(module_slug, result=None, user=user)
#         if advice:
#             events.append({
#                 "type": "mentor_tip",
#                 "delivery": "overlay",
#                 "message": advice,
#                 "icon": "Lightbulb",
#                 "color": "neon-blue"
#             })
        
#         return events

#     @staticmethod
#     def dispatch_events(user_id: int, events: List[Dict[str, Any]]):
#         """
#         Routes events to correct delivery systems and emits SocketIO.
#         """
#         for event in events:
#             # Persistent DB Notifications
#             if event["delivery"] == "notification":
#                 ExperienceEngine._create_persistent_notification(user_id, event)
            
#             # Real-time UI feedback (Toasts/Overlays)
#             # We emit everything via common ux_event, but frontend routes based on delivery
#             try:
#                 socketio.emit(
#                     "ux_event",
#                     event,
#                     room=f"user_{user_id}"
#                 )
#             except Exception as e:
#                 logger.error(f"Failed to emit socket event: {e}")

#     @staticmethod
#     def _create_persistent_notification(user_id: int, event: Dict[str, Any]):
#         """Helper to create persistent notifications via service."""
#         NotificationService.create_notification(
#             user_id=user_id,
#             title=event.get("title", "New Update"),
#             message=event.get("message", ""),
#             type_=event.get("category", "info")
#         )

# experience_engine = ExperienceEngine()
