"""
File: app/api/routes/profile_routes.py

Profile routes (FastAPI - production ready)
"""

import os
import time
import shutil
from fastapi import APIRouter, Depends, HTTPException, Request, Body, UploadFile, File
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.utils.auth_decorators import get_current_user
from app.core.redis_client import neural_cache

from app.domain.profile_service import UserProfileService
from app.schemas.profile_schema import FullProfileResponse, DashboardResponse

profile_router = APIRouter()

# ---------------------------------------------------------

# GET PROFILE

# ---------------------------------------------------------

@profile_router.get("/me", response_model=FullProfileResponse)
async def get_my_profile(
db: Session = Depends(get_db),
user: User = Depends(get_current_user)
):
    user = db.get(User, user.id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    profile = UserProfileService.format_user_profile(db, user)
    stats = UserProfileService.get_user_statistics(db, user)
    achievements = UserProfileService.get_user_achievements(db, user)

    return {
            "profile": {
                "id": profile.user_id,
                "username": profile.username,
                "email": profile.email,
                "first_name": profile.first_name,
                "last_name": profile.last_name,
                "avatar_url": profile.avatar_url,
                "bio": profile.bio,
                "joined_date": profile.joined_date,
            },
            "statistics": stats,
            "achievements": achievements,
        }

    # ---------------------------------------------------------

    # UPDATE PROFILE

    # ---------------------------------------------------------

@profile_router.put("/me")
async def update_my_profile(
payload: dict = Body(...),
user: User = Depends(get_current_user),
db: Session = Depends(get_db)
):
    user = db.get(User, user.id)
    if not user:
            raise HTTPException(status_code=404, detail="User not found")

    profile = UserProfileService.update_profile(
        db,
        user,
        first_name=payload.get("first_name"),
        last_name=payload.get("last_name"),
        bio=payload.get("bio"),
        avatar_url=payload.get("avatar_url"),
    )

    return {"message": "Profile updated successfully", "profile": profile}

    # ---------------------------------------------------------

    # UPLOAD AVATAR

    # ---------------------------------------------------------

@profile_router.post("/avatar")
async def upload_avatar(
request: Request,
avatar: UploadFile = File(...),
user: User = Depends(get_current_user),
db: Session = Depends(get_db)
):
    user = db.get(User, user.id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    clean_filename = "".join(c for c in avatar.filename if c.isalnum() or c in "._-")

    upload_dir = os.path.join("app", "static", "uploads", "avatars")
    os.makedirs(upload_dir, exist_ok=True)

    unique_name = f"{user.id}_{int(time.time())}_{clean_filename}"
    save_path = os.path.join(upload_dir, unique_name)

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(avatar.file, buffer)

    base_url = str(request.base_url).rstrip("/")
    avatar_url = f"{base_url}/static/uploads/avatars/{unique_name}"

    UserProfileService.update_avatar(db, user, avatar_url)

    return {"success": True, "avatar_url": avatar_url}
    

    # ---------------------------------------------------------

    # DASHBOARD

    # ---------------------------------------------------------

@profile_router.get("/me/dashboard-summary", response_model=DashboardResponse)
async def get_dashboard_summary(
user: User = Depends(get_current_user),
db: Session = Depends(get_db)
):
    cache_key = f"user:{user.id}:dashboard-summary"

    cached = neural_cache.get(cache_key)
    if cached:
        return cached

    user = db.get(User, user.id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    from app.domain.progression_service import ProgressionService
    from app.domain.quest_service import QuestService

    progression = ProgressionService.get_user_progression(db, user.id)
    quests = QuestService.get_active_quests(db, user.id)

    formatted_quests = [
        {
            "id": q.id,
            "task": q.quest.title,
            "reward": f"{q.quest.xp_reward} XP",
            "progress": int((q.progress / q.quest.target_score) * 100) if q.quest.target_score else 0,
            "color": "neon-blue"
        }
        for q in quests
    ] or [
        {"id": 101, "task": "Complete your first module", "reward": "100 XP", "progress": 0, "color": "neon-pink"}
    ]

    stats = UserProfileService.get_user_statistics(db, user)
    age_days = stats.get("account_age_days", 0)

    response = {
        "xp": progression.total_xp,
        "level": progression.level,
        "rank": progression.rank_title,
        "title": progression.rank_title.upper(),
        "uptime": f"{age_days * 24}h",
        "performance_history": stats.get("performance_history", []),
        "recent_activity": UserProfileService.get_recent_activity(db, user),
        "daily_quests": formatted_quests,
        "user": {
            "username": user.username or user.email.split("@")[0],
            "avatar": user.avatar_url,
            "role": user.role.name if user.role else "user"
        }
    }

    neural_cache.set(cache_key, response, ex=30)
    return response

    # ---------------------------------------------------------

    # FEEDBACK

    # ---------------------------------------------------------

@profile_router.post("/feedback", status_code=201)
async def submit_feedback(
payload: dict = Body(...),
user: User = Depends(get_current_user),
db: Session = Depends(get_db)
):
    message = payload.get("message")
    rating = payload.get("rating")

    
    if not message or rating is None:
        raise HTTPException(status_code=400, detail="Message and rating are required")

    UserProfileService.submit_feedback(db, user.id, message, rating)

    return {"success": True}


# import os
# import time
# import shutil
# from fastapi import APIRouter, Depends, HTTPException, Request, Response, Body, UploadFile, File, Form
# from typing import Optional, List
# from sqlalchemy.orm import Session
# from app.core.database import get_db
# from app.models.user import User
# from app.domain.profile_service import UserProfileService
# from app.utils.auth_decorators import get_current_user

# from app.core.config import settings

# from app.core.redis_client import neural_cache

# profile_router = APIRouter()
# # @auth_router.post("/login")
# # async def login(
# #     response: Response,
# #     request: Request,
# #     payload: dict = Body(...),
# #     db: Session = Depends(get_db)
# # ):
# # ---------------------------------------------

# # FIXED: Proper FastAPI DI usage

# # ---------------------------------------------

# @profile_router.get("/me")
# async def get_my_profile(
# db: Session = Depends(get_db),
# user: User = Depends(get_current_user)
# ):
#     """Get current user's profile."""

#     user = db.get(User, user.id)

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     profile = UserProfileService.format_user_profile(user)

#     # FIXED: pass db
#     stats = UserProfileService.get_user_statistics(db, user)

#     achievements = UserProfileService.get_user_achievements(user)

#     return {
#         "profile": {
#             "id": profile.user_id,
#             "username": profile.username,
#             "email": profile.email,
#             "first_name": profile.first_name,
#             "last_name": profile.last_name,
#             "avatar_url": profile.avatar_url,
#             "bio": profile.bio,
#             "joined_date": profile.joined_date,
#         },
#         "statistics": stats,
#         "achievements": achievements,
#     }

# @profile_router.put("/me")
# async def update_my_profile(
#     payload: dict = Body(...), user : User = Depends(get_current_user), db: Session = Depends(get_db)):
#     """Update current user's profile."""
#     user_id = user.id
#     user = db.get(User, user_id)

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     profile = UserProfileService.update_profile(
#         db,        
#         user,
#         first_name=payload.get("first_name"),
#         last_name=payload.get("last_name"),
#         bio=payload.get("bio"),
#         avatar_url=payload.get("avatar_url"),
#     )

#     return {
#         "message": "Profile updated successfully",
#         "profile": {
#             "id": profile.user_id,
#             "username": profile.username,
#             "email": profile.email,
#             "first_name": profile.first_name,
#             "last_name": profile.last_name,
#             "avatar_url": profile.avatar_url,
#             "bio": profile.bio,
#         },
#     }

# @profile_router.post("/avatar")
# async def upload_avatar(
#     request: Request, avatar: UploadFile = File(...), user : User = Depends(get_current_user), db: Session = Depends(get_db)
# ):
#     """Upload user avatar image."""
#     user_id = user.id
#     user = db.get(User, user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     # Save file
#     # Note: Using a minimal secure filename approach
#     clean_filename = "".join([c for c in avatar.filename if c.isalnum() or c in "._-"])
#     upload_dir = os.path.join("app", "static", "uploads", "avatars")
#     os.makedirs(upload_dir, exist_ok=True)

#     unique_name = f"{user_id}_{int(time.time())}_{clean_filename}"
#     save_path = os.path.join(upload_dir, unique_name)
    
#     with open(save_path, "wb") as buffer:
#         shutil.copyfileobj(avatar.file, buffer)

#     # Generate URL (compatible with frontend expectation)
#     # Using relative URL for simplicity if base URL is handled by frontend or proxy
#     base_url = str(request.base_url).rstrip("/")
#     avatar_url = f"{base_url}/static/uploads/avatars/{unique_name}"

#     UserProfileService.update_avatar(user, avatar_url)

#     return {"success": True, "avatar_url": avatar_url}

# @profile_router.get("/me/stats")
# async def get_user_statistics(
#     user : User = Depends(get_current_user), db: Session = Depends(get_db)):
#     """Get user statistics."""
#     user_id = user.id
#     user = db.get(User, user_id)

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     stats = UserProfileService.get_user_statistics(db, user)
#     return {"statistics": stats}

# @profile_router.get("/me/achievements")
# async def get_user_achievements(user : User = Depends(get_current_user), db: Session = Depends(get_db)  ):
#     """Get user achievements."""
#     user_id = user.id
#     user = db.get(User, user_id)

#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     achievements = UserProfileService.get_user_achievements(user)
#     return {"achievements": achievements}

# @profile_router.get("/me/dashboard-summary")
# async def get_dashboard_summary(
#     user : User = Depends(get_current_user),
#     db: Session = Depends(get_db)):
#     """Unified endpoint for user dashboard content."""
#     user_id = user.id
    
#     cache_key = f"user:{user_id}:dashboard-summary"
#     cached_data = neural_cache.get(cache_key)
#     if cached_data:
#         return cached_data

#     user = db.get(User, user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     from app.domain.progression_service import ProgressionService
#     from app.domain.quest_service import QuestService

#     progression = ProgressionService.get_user_progression(db,user.id)
#     active_quests = QuestService.get_active_quests(db, user.id)
    
#     formatted_quests = []
#     for uq in active_quests:
#         formatted_quests.append({
#             "id": uq.id,
#             "task": uq.quest.title,
#             "reward": f"{uq.quest.xp_reward} XP",
#             "progress": int((uq.progress / uq.quest.target_score) * 100) if uq.quest.target_score > 0 else 0,
#             "color": "neon-blue"
#         })

#     if not formatted_quests:
#         formatted_quests = [
#             {"id": 101, "task": "Complete your first module", "reward": "100 XP", "progress": 0, "color": "neon-pink"},
#         ]

#     stats = UserProfileService.get_user_statistics(db, user) or {}
#     age_days = int(stats.get('account_age_days') or 0)

#     response_data = {
#         "xp": progression.total_xp,
#         "level": progression.level,
#         "rank": progression.rank_title,
#         "title": progression.rank_title.upper(),
#         "uptime": f"{age_days * 24}h",
#         "performance_history": stats.get("performance_history", []),
#         "recent_activity": UserProfileService.get_recent_activity(user),
#         "daily_quests": formatted_quests,
#         "user": {
#             "username": user.username or (user.email.split('@')[0] if user.email else "user"),
#             "avatar": getattr(user, 'avatar_url', None),
#             "role": str(user.role.name) if (user.role and hasattr(user.role, 'name')) else "user"
#         }
#     }
    
#     neural_cache.set(cache_key, response_data, ex=30)
#     return response_data

# @profile_router.post("/feedback", status_code=201)
# async def submit_feedback(payload: dict = Body(...), user : User = Depends(get_current_user)):
#     """Submit feedback for the current user."""
#     message = payload.get("message")
#     rating = payload.get("rating")

#     if not message or rating is None:
#         raise HTTPException(status_code=400, detail="Message and rating are required")

#     user_id = user.id
#     UserProfileService.submit_feedback(user_id, message, rating)
#     return {"success": True, "message": "Feedback recorded"}
