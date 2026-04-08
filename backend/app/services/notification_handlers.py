from app.services.notification_service import NotificationService
from app.domain.event_bus import EventBus, Events

def handle_xp_granted(data):
    print("XP HANDLER TRIGGERED")
    db = data.get("db")
    if not db: return

    user_id = data["user_id"]
    xp = data.get("xp_awarded", 0)
    module_name = data.get("module_name", "a module")

    NotificationService.create_notification(
        db=db, user_id=user_id, title="XP Earned",
        message=f"+{xp} XP from {module_name}", type_="credit",
        data={"xp": xp, "module": module_name},
        # icon="Zap", color="neon-blue"
    )

def handle_level_up(data):
    db = data.get("db")
    if not db: return

    user_id = data["user_id"]
    level = data.get("level") or data.get("new_level")

    NotificationService.create_notification(
        db=db, user_id=user_id, title="Level Up!",
        message=f"You reached Level {level}.", type_="achievement",
        data={"level": level}, 
        # icon="Star", color="neon-pink"
    )

def handle_streak_updated(data):
    db = data.get("db")
    if not db: return

    NotificationService.create_notification(
        db=db, user_id=data["user_id"], title="Daily Streak \U0001f525",
        message=f"You are on a {data['streak']} day streak!",
        type_="achievement", 
        # icon="Flame", color="neon-orange"
    )

def handle_quest_completed(data):
    db = data.get("db")
    if not db: return

    user_id = data["user_id"]
    title = data.get("quest_title")
    xp = data.get("xp_reward", 0)

    NotificationService.create_notification(
        db=db, user_id=user_id, title="Quest Completed!",
        message=f"You finished '{title}' and earned {xp} XP.",
        type_="achievement", 
        # icon="CheckCircle", color="neon-green"
    )

_HANDLERS_REGISTERED = False

def register_notification_handlers():
    global _HANDLERS_REGISTERED
    if _HANDLERS_REGISTERED: return

    EventBus.subscribe(Events.XP_GRANTED, handle_xp_granted)
    EventBus.subscribe(Events.LEVEL_UP, handle_level_up)
    EventBus.subscribe(Events.STREAK_UPDATED, handle_streak_updated)
    EventBus.subscribe(Events.QUEST_COMPLETED, handle_quest_completed)
    
    _HANDLERS_REGISTERED = True
    print("NOTIFICATION_HANDLERS_REGISTERED in services")
