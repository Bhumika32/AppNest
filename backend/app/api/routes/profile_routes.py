#app/api/routes/profile_routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps.auth import get_current_user

from app.core.cache_service import CacheService
from app.repositories.module_repository import ModuleRepository
from app.repositories.user_repository import user_repository
from app.repositories.game_session_repository import game_session_repository
from app.repositories.progression_repository import ProgressionRepository
from app.repositories.xp_transaction_repository import XPTransactionRepository

from app.services.profile_service import UserProfileService

from app.schemas.profile_schema import FullProfileResponse, DashboardResponse

profile_router = APIRouter()


def get_profile_service():
    return UserProfileService(
        user_repository,
        game_session_repository,
        ProgressionRepository(),
        XPTransactionRepository(),
        ModuleRepository()
    )


@profile_router.get("/me", response_model=FullProfileResponse)
async def get_my_profile(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    service: UserProfileService = Depends(get_profile_service)
):
    try:
        profile = service.get_profile(db, user.id)
        stats = service.get_statistics(db, user.id)
        achievements = service.get_achievements(stats)

        return FullProfileResponse(
            profile=profile.__dict__,
            statistics=stats,
            achievements=achievements
        )

    except ValueError:
        raise HTTPException(404, "User not found")


@profile_router.get("/me/dashboard-summary", response_model=DashboardResponse)
async def get_dashboard_summary(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    service: UserProfileService = Depends(get_profile_service)
):
    cache_key = CacheService.build_key("dashboard", str(user.id))

    cached = CacheService.get_json(cache_key)
    if cached:
        return DashboardResponse(**cached)

    stats = service.get_statistics(db, user.id)
    activity = service.get_recent_activity(db, user.id)

    response = {
        "xp": stats["xp"],
        "level": stats["level"],
        "rank": "Rookie",  # TEMP until progression fix
        "theme": "default",
        "title": "ROOKIE",
        "uptime": f"{stats['account_age_days'] * 24}h",
        "performance_history": stats["performance_history"],
        "recent_activity": activity,
        "daily_quests": [],
        "user": {
            "username": user.username,
            "avatar": user.avatar_url,
            "role": "user"
        }
    }

    CacheService.set_json(cache_key, response, ttl=30)

    return DashboardResponse(**response)
