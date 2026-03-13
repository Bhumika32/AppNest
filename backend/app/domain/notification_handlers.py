"""
File: backend/app/domain/notification_handlers.py

Event-driven notification handlers for AppNest.
Only meaningful long-term events are persisted as notifications.

Rules:
- XP notifications represent module completion.
- Do NOT store roast or mentor feedback in DB.
- Do NOT store MODULE_COMPLETED notifications (XP already implies completion).
"""

from app.domain.notification_service import NotificationService
from app.domain.event_bus import EventBus, Events


# ---------------------------------------------------------
# XP EARNED NOTIFICATION
# ---------------------------------------------------------

def handle_xp_granted(data):
    """Create notification when XP is granted."""

    user_id = data["user_id"]
    xp = data.get("xp_awarded", 0)
    module_name = data.get("module_name", "a module")

    NotificationService.create_notification(
        user_id=user_id,
        title="XP Earned",
        message=f"+{xp} XP from {module_name}",
        type_="credit",
        data={
            "xp": xp,
            "module": module_name
        },
        icon="Zap",
        color="neon-blue"
    )


# ---------------------------------------------------------
# LEVEL UP NOTIFICATION
# ---------------------------------------------------------

def handle_level_up(data):
    """Create notification when a user levels up."""

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


# ---------------------------------------------------------
# STREAK UPDATED
# ---------------------------------------------------------

def handle_streak_updated(data):
    """Create notification when a daily streak updates."""

    NotificationService.create_notification(
        user_id=data["user_id"],
        title="Daily Streak 🔥",
        message=f"You are on a {data['streak']} day streak!",
        type_="achievement",
        icon="Flame",
        color="neon-orange"
    )


# ---------------------------------------------------------
# QUEST COMPLETED
# ---------------------------------------------------------

def handle_quest_completed(data):
    """Create notification when a quest is completed."""

    user_id = data["user_id"]
    title = data.get("quest_title")
    xp = data.get("xp_reward", 0)

    NotificationService.create_notification(
        user_id=user_id,
        title="Quest Completed!",
        message=f"You finished '{title}' and earned {xp} XP.",
        type_="achievement",
        icon="CheckCircle",
        color="neon-green"
    )


# ---------------------------------------------------------
# REGISTER EVENT LISTENERS
# ---------------------------------------------------------

def register_notification_handlers():
    """Register notification listeners with the EventBus."""

    EventBus.subscribe(Events.XP_GRANTED, handle_xp_granted)
    EventBus.subscribe(Events.LEVEL_UP, handle_level_up)
    EventBus.subscribe(Events.STREAK_UPDATED, handle_streak_updated)
    EventBus.subscribe(Events.QUEST_COMPLETED, handle_quest_completed)


print("NOTIFICATION_HANDLERS_REGISTERED")
    # These are now managed centrally by ExperienceEngine
    # EventBus.subscribe(Events.MODULE_COMPLETED, handle_module_completed)
    # EventBus.subscribe(Events.XP_GRANTED, handle_xp_granted)
    # EventBus.subscribe(Events.LEVEL_UP, handle_level_up)
    # EventBus.subscribe(Events.STREAK_UPDATED, handle_streak_updated)
    # EventBus.subscribe(Events.ROAST_GENERATED, handle_roast_generated)
    # EventBus.subscribe(Events.MENTOR_ADVICE_GIVEN, handle_mentor_advice)
    # EventBus.subscribe(Events.QUEST_COMPLETED, handle_quest_completed)
    # pass
