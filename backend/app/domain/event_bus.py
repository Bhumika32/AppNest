# -----------------------------------------------------------------------------
# File: backend/app/domain/event_bus.py
# -----------------------------------------------------------------------------
# Description:
# Core domain event bus for AppNest.
#
# This system allows different services to communicate without tight coupling.
# For example:
#   LifecycleService → publishes XP_GRANTED
#   notification_handlers → listens and creates notifications
#
# Major Fix Implemented:
# ----------------------
# Prevent duplicate event subscriptions. Flask debug reloader can execute
# application startup twice which previously caused the same handler to be
# registered multiple times. That resulted in duplicate notifications.
#
# The subscribe() method now checks if the callback already exists.
# -----------------------------------------------------------------------------

from typing import Callable, Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class BaseEventDispatcher:
    """
    Interface for event bus implementations.
    """

    def subscribe(self, event_type: str, callback: Callable) -> None:
        raise NotImplementedError

    def publish(self, event_type: str, data: Any = None) -> None:
        raise NotImplementedError


class InMemoryEventBus(BaseEventDispatcher):
    """
    Simple in-memory publish/subscribe event bus.

    Suitable for development and single-instance deployments.
    Future upgrade path: RedisEventBus for distributed workers.
    """

    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}

    # -------------------------------------------------------------------------
    # SUBSCRIBE
    # -------------------------------------------------------------------------
    def subscribe(self, event_type: str, callback: Callable) -> None:
        """
        Register an event handler.

        This method prevents duplicate registration which can happen
        when Flask debug reloader runs application startup twice.
        """

        if event_type not in self._subscribers:
            self._subscribers[event_type] = []

        # Prevent duplicate handler registration
        if callback not in self._subscribers[event_type]:
            self._subscribers[event_type].append(callback)
        else:
            logger.debug(
                f"Duplicate event subscription ignored for {event_type}: {callback}"
            )

    # -------------------------------------------------------------------------
    # PUBLISH
    # -------------------------------------------------------------------------
    def publish(self, event_type: str, data: Any = None) -> None:
        """
        Publish an event to all subscribers.
        """

        subscribers = self._subscribers.get(event_type, [])

        if not subscribers:
            logger.debug(f"No subscribers registered for event {event_type}")
            return

        for callback in subscribers:
            try:
                callback(data)
            except Exception as e:
                logger.error(
                    f"Error in event subscriber for {event_type}: {e}"
                )


# -----------------------------------------------------------------------------
# GLOBAL EVENT BUS INSTANCE
# -----------------------------------------------------------------------------

# Global singleton used across the application
EventBus = InMemoryEventBus()


# -----------------------------------------------------------------------------
# EVENT CONSTANTS
# -----------------------------------------------------------------------------

class Events:
    """
    Domain event identifiers used across services.
    """

    MODULE_COMPLETED = "MODULE_COMPLETED"
    XP_GRANTED = "XP_GRANTED"
    LEVEL_UP = "LEVEL_UP"
    LEVEL_MILESTONE = "LEVEL_MILESTONE"

    ACHIEVEMENT_UNLOCKED = "ACHIEVEMENT_UNLOCKED"
    STREAK_UPDATED = "STREAK_UPDATED"

    ROAST_GENERATED = "ROAST_GENERATED"
    MENTOR_ADVICE_GIVEN = "MENTOR_ADVICE_GIVEN"

    QUEST_COMPLETED = "QUEST_COMPLETED"
    LEADERBOARD_UPDATED = "LEADERBOARD_UPDATED"
