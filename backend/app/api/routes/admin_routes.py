from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session as DBSession

from app.domain.analytics_service import AnalyticsService
from app.models.module import Module
from app.core.redis_client import neural_cache
from app.utils.auth_decorators import get_admin_user
from app.models.user import User
from app.core.database import get_db


admin_router = APIRouter()


# ---------------------------------------------------------
# MODULE MANAGEMENT
# ---------------------------------------------------------

@admin_router.get("/modules")
async def get_admin_modules(
    db: DBSession = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    """Get all registered modules for admin management."""
    modules = db.query(Module).all()
    return [m.to_dict() for m in modules]


@admin_router.patch("/modules/{id}")
async def update_module_status(
    id: int,
    data: dict = Body(...),
    db: DBSession = Depends(get_db),
    admin: User = Depends(get_admin_user)
):
    """Enable/disable or update module metadata."""

    module = db.get(Module, id)

    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    if "is_active" in data:
        module.is_active = data["is_active"]

    db.commit()

    return module.to_dict()


# ---------------------------------------------------------
# ANALYTICS: PLATFORM OVERVIEW
# ---------------------------------------------------------

@admin_router.get("/analytics/overview")
async def get_overview(
    db: DBSession = Depends(get_db),
    admin: User = Depends(get_admin_user)
):

    cache_key = "admin:analytics:overview"

    stats = neural_cache.get(cache_key)

    if not stats:
        stats = AnalyticsService.get_platform_stats(db)
        neural_cache.set(cache_key, stats, ex=300)

    return stats


# ---------------------------------------------------------
# ANALYTICS: USER GROWTH
# ---------------------------------------------------------

@admin_router.get("/analytics/users")
async def get_user_analytics(
    db: DBSession = Depends(get_db),
    admin: User = Depends(get_admin_user)
):

    cache_key = "admin:analytics:users"

    user_data = neural_cache.get(cache_key)

    if not user_data:
        user_data = AnalyticsService.get_user_growth_data(db)
        neural_cache.set(cache_key, user_data, ex=300)

    return user_data


# ---------------------------------------------------------
# ANALYTICS: GAME POPULARITY
# ---------------------------------------------------------

@admin_router.get("/analytics/games")
async def get_game_analytics(
    db: DBSession = Depends(get_db),
    admin: User = Depends(get_admin_user)
):

    cache_key = "admin:analytics:games"

    game_data = neural_cache.get(cache_key)

    if not game_data:
        game_data = AnalyticsService.get_game_popularity(db)
        neural_cache.set(cache_key, game_data, ex=300)

    return game_data


# ---------------------------------------------------------
# ANALYTICS: TOOL USAGE
# ---------------------------------------------------------

@admin_router.get("/analytics/tools")
async def get_tool_analytics(
    db: DBSession = Depends(get_db),
    admin: User = Depends(get_admin_user)
):

    cache_key = "admin:analytics:tools"

    tool_data = neural_cache.get(cache_key)

    if not tool_data:
        tool_data = AnalyticsService.get_tool_usage(db)
        neural_cache.set(cache_key, tool_data, ex=300)

    return tool_data


# from fastapi import APIRouter, Depends, HTTPException, status, Body
# from app.domain.analytics_service import AnalyticsService
# from app.models.module import Module
# from sqlalchemy.orm import Session as DBSession
# from app.core.redis_client import neural_cache
# from app.utils.auth_decorators import get_admin_user
# from app.models.user import User
# from app.core.database import get_db

# admin_router = APIRouter()

# @admin_router.get("/modules")
# async def get_admin_modules(
#     db: DBSession = Depends(get_db),
#     admin: User = Depends(get_admin_user)):
#     """Get all registered modules for admin management."""
#     modules = db.query(Module).all()
#     return [m.to_dict() for m in modules]


# @admin_router.patch("/modules/{id}")
# async def update_module_status( db: DBSession = Depends(get_db), data: dict = Body(...), admin: User = Depends(get_admin_user)):
#     """Enable/disable or update module metadata."""
#     module = db.get(Module, id)
#     if not module:
#         raise HTTPException(status_code=404, detail="Module not found")

#     if 'is_active' in data:
#         module.is_active = data['is_active']
    
#     db.flush()
#     return module.to_dict()

# @admin_router.get('/analytics/overview')
# async def get_overview(admin: User = Depends(get_admin_user)):
#     cache_key = "admin:analytics:overview"
#     stats = neural_cache.get(cache_key)
#     if not stats:
#         stats = AnalyticsService.get_platform_stats()
#         neural_cache.set(cache_key, stats, ex=300)
#     return stats

# @admin_router.get('/analytics/users')
# async def get_user_analytics(admin: User = Depends(get_admin_user)):
#     cache_key = "admin:analytics:users"
#     user_data = neural_cache.get(cache_key)
#     if not user_data:
#         user_data = AnalyticsService.get_user_growth_data()
#         neural_cache.set(cache_key, user_data, ex=300)
#     return user_data

# @admin_router.get('/analytics/games')
# async def get_game_analytics(admin: User = Depends(get_admin_user)):
#     cache_key = "admin:analytics:games"
#     game_data = neural_cache.get(cache_key)
#     if not game_data:
#         game_data = AnalyticsService.get_game_popularity()
#         neural_cache.set(cache_key, game_data, ex=300)
#     return game_data

# @admin_router.get('/analytics/tools')
# async def get_tool_analytics(admin: User = Depends(get_admin_user)):
#     cache_key = "admin:analytics:tools"
#     tool_data = neural_cache.get(cache_key)
#     if not tool_data:
#         tool_data = AnalyticsService.get_tool_usage()
#         neural_cache.set(cache_key, tool_data, ex=300)
#     return tool_data

