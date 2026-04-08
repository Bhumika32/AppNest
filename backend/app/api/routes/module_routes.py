"""
File: app/api/routes/module_routes.py

Module routes including:
- Module listing
- Module execution
- Leaderboards (global + module-specific)
- Analytics tracking
"""

from fastapi import APIRouter, Depends, HTTPException, Query, Body, status
from typing import Optional
from sqlalchemy.orm import Session

from app.services.module_service import ModuleService, get_module_service
from app.services.leaderboard_service import LeaderboardService, get_leaderboard_service
from app.domain.lifecycle_service import LifecycleService

from app.schemas.module_schema import (
    ModuleResponse,
    ModuleListResponse,
    GlobalLeaderboardResponse,
    ModuleLeaderboardResponse,
    GlobalLeaderboardEntry,
    ModuleLeaderboardEntry,
    StartTrackingResponse,
    SimpleMessageResponse,
)

from app.api.deps.auth import get_current_user, get_admin_user
from app.core.database import get_db
from app.models.user import User


module_router = APIRouter()
admin_module_router = APIRouter()

# -----------------------------
# MODULE LIST
# -----------------------------
@module_router.get("", response_model=ModuleListResponse)
async def get_modules(
    type: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    service: ModuleService = Depends(get_module_service)
):
    modules = service.get_all_modules(db, type)

    return ModuleListResponse(
        modules=[ModuleResponse.model_validate(m) for m in modules]
    )
# -----------------------------
# MODULE DETAILS
# -----------------------------
@module_router.get("/slug/{slug}", response_model=ModuleResponse)
async def get_module_by_slug(
    slug: str,
    db: Session = Depends(get_db),
    service: ModuleService = Depends(get_module_service)
):
    try:
        module = service.get_module_by_slug(db, slug)
        return ModuleResponse.model_validate(module)
    except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
    
# -----------------------------
# MODULE EXECUTION ( CRITICAL FIX)
# -----------------------------
@module_router.post("/execute/{slug}")
async def execute_module(
    slug: str,
    payload: dict = Body(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    service: ModuleService = Depends(get_module_service)
):
    try:
        result = service.execute_module(
            db=db,
            user_id=user.id,
            slug=slug,
            payload=payload
        )

        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# -----------------------------
# ANALYTICS START
# -----------------------------
@module_router.post("/analytics/start", response_model=StartTrackingResponse)
async def track_start(
    payload: dict = Body(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    service: ModuleService = Depends(get_module_service)
):
    module_id = payload.get("module_id")

    if not module_id:
        raise HTTPException(status_code=400, detail="module_id required")

    try:
        entry_id = service.track_start(db, user.id, module_id)
        return StartTrackingResponse(
            message="Launch tracked",
            entry_id=entry_id
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


# -----------------------------
# ANALYTICS END
# -----------------------------
@module_router.post("/analytics/end", response_model=SimpleMessageResponse)
async def track_end(
    payload: dict = Body(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    service: ModuleService = Depends(get_module_service)
):
    entry_id = payload.get("entry_id")
    duration = payload.get("duration", 0)

    if not entry_id:
        raise HTTPException(status_code=400, detail="entry_id required")

    try:
        service.track_end(db, user.id, entry_id, duration)
        return SimpleMessageResponse(message="Session finalized")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# -----------------------------
# GLOBAL LEADERBOARD
# -----------------------------
@module_router.get("/leaderboard", response_model=GlobalLeaderboardResponse)
async def get_global_leaderboard(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    service: LeaderboardService = Depends(get_leaderboard_service)
):
    rankings = service.get_global_rankings(db, limit)

    return GlobalLeaderboardResponse(
        rankings=[GlobalLeaderboardEntry.model_validate(r) for r in rankings]
    )

# -----------------------------
# MODULE LEADERBOARD
# -----------------------------
@module_router.get("/{slug}/leaderboard", response_model=ModuleLeaderboardResponse)
async def get_module_leaderboard(
    slug: str,
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    service: LeaderboardService = Depends(get_leaderboard_service)
):
    rankings = service.get_module_rankings(db, slug, limit)

    return ModuleLeaderboardResponse(
        rankings=[ModuleLeaderboardEntry.model_validate(r) for r in rankings]
    )
