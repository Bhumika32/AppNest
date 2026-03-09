from typing import Callable, Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class BaseEventDispatcher:
    """Interface for event bus implementations."""
    def subscribe(self, event_type: str, callback: Callable) -> None:
        raise NotImplementedError

    def publish(self, event_type: str, data: Any = None) -> None:
        raise NotImplementedError

class InMemoryEventBus(BaseEventDispatcher):
    """Simple in-memory publish/subscribe event bus."""
    
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, callback: Callable) -> None:
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def publish(self, event_type: str, data: Any = None) -> None:
        subscribers = self._subscribers.get(event_type, [])
        for callback in subscribers:
            try:
                callback(data)
            except Exception as e:
                logger.error(f"Error in event subscriber for {event_type}: {e}")

# Global instance for backward compatibility
# In the future, this can be swapped with RedisEventBus()
EventBus = InMemoryEventBus()

# Predefine some event constants
class Events:
    MODULE_COMPLETED = "MODULE_COMPLETED"
    XP_GRANTED = "XP_GRANTED"
    LEVEL_UP = "LEVEL_UP"
    ACHIEVEMENT_UNLOCKED = "ACHIEVEMENT_UNLOCKED"
    STREAK_UPDATED = "streak_updated"