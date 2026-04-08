# File: app/domain/event_bus.py

from typing import Callable, Dict, List, Any
import logging

logger = logging.getLogger(__name__)


class BaseEventDispatcher:
    def subscribe(self, event_type: str, callback: Callable) -> None:
        raise NotImplementedError

    def publish(self, event_type: str, data: Any = None) -> None:
        raise NotImplementedError


class InMemoryEventBus(BaseEventDispatcher):

    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, callback: Callable) -> None:

        if event_type not in self._subscribers:
            self._subscribers[event_type] = []

        if callback not in self._subscribers[event_type]:
            self._subscribers[event_type].append(callback)
        else:
            logger.debug(f"Duplicate subscription ignored: {event_type}")

    def publish(self, event_type: str, data: Any = None) -> None:

        subscribers = self._subscribers.get(event_type, [])

        if not subscribers:
            logger.debug(f"No subscribers for event {event_type}")
            return

        for callback in subscribers:
            try:
                callback(data)
            except Exception:
                logger.exception(f"Error in event handler for {event_type}")


# -----------------------------
# GLOBAL SINGLETON (THIS WAS MISSING)
# -----------------------------
_event_bus = InMemoryEventBus()


class EventBus:
    """
    Stateless wrapper over global event bus
    """

    @staticmethod
    def publish(event_type: str, data: Any = None):
        _event_bus.publish(event_type, data)

    @staticmethod
    def subscribe(event_type: str, callback: Callable):
        _event_bus.subscribe(event_type, callback)


# -----------------------------
# EVENT CONSTANTS
# -----------------------------
class Events:
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