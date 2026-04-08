# Import all models here so Alembic can detect them for migrations
from app.models.user import User
from app.models.role import Role
from app.models.session import Session
from app.models.otp_token import OTPToken
from app.models.feedback import Feedback
from app.models.game_session import GameSession
# Standardizing common model imports
from app.models.achievement import Achievement
from app.models.user_achievement import UserAchievement
from app.models.module import Module
from app.models.module_analytics import ModuleAnalytics
from app.models.notification import Notification
from app.models.user_progression import UserProgression
from app.models.xp_transaction import XPTransaction
from app.models.quest import Quest
from app.models.user_quest import UserQuest
from app.models.leaderboard import Leaderboard