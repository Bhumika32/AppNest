"""
Notification Event Handlers

Subscribes to EventBus events and converts them into user notifications.
This keeps the system event-driven and decoupled.
"""

from app.services.notification_service import NotificationService
from app.services.event_bus import EventBus, Events


def handle_module_completed(data):
    """Notification for module completion."""
    user_id = data["user_id"]
    module_id = data.get("module_id")
    score = data.get("score", 0)

    NotificationService.create_notification(
        user_id=user_id,
        title="Module Completed",
        message=f"You completed a module and scored {score} points.",
        type_="achievement",
        icon="Trophy",
        color="neon-blue"
    )


def handle_xp_granted(data):
    """Notification for XP reward."""
    user_id = data["user_id"]
    xp = data.get("xp_awarded", 0)

    NotificationService.create_notification(
        user_id=user_id,
        title="XP Earned",
        message=f"You gained {xp} XP.",
        type_="credit",
        data={"xp": xp},
        icon="Zap",
        color="neon-blue"
    )


def handle_level_up(data):
    """Notification for level up."""
    user_id = data["user_id"]
    level = data.get("new_level")

    NotificationService.create_notification(
        user_id=user_id,
        title="Level Up!",
        message=f"You reached Level {level}.",
        type_="achievement",
        data={"level": level},
        icon="Star",
        color="neon-pink"
    )
def handle_streak_updated(data):
    NotificationService.create_notification(
        user_id=data["user_id"],
        title="Daily Streak 🔥",
        message=f"You are on a {data['streak']} day streak!",
        type_="achievement",
        icon="Flame",
        color="neon-orange"
    )

def register_notification_handlers():
    """Register all notification listeners."""
    
    EventBus.subscribe(Events.MODULE_COMPLETED, handle_module_completed)
    EventBus.subscribe(Events.XP_GRANTED, handle_xp_granted)
    EventBus.subscribe(Events.LEVEL_UP, handle_level_up)
    EventBus.subscribe(Events.STREAK_UPDATED, handle_streak_updated)