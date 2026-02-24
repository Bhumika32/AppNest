# Import all models here so Alembic can detect them for migrations
from app.models.user import User
from app.models.role import Role
from app.models.session import Session
from app.models.otp_token import OTPToken
from app.models.feedback import Feedback
from app.models.game_session import GameSession
from app.models.achievement import Achievement
from app.models.profile_metric import ProfileMetric
from app.models.module import Module, ModuleAnalytics
from app.models.notification import Notification