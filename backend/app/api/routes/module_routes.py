from fastapi import APIRouter, Depends, HTTPException, Query, Request, Body, status
from typing import List, Optional
from app.domain.module_service import ModuleService
from app.domain.lifecycle_service import LifecycleService
from app.utils.auth_decorators import get_current_user, get_admin_user
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User

module_router = APIRouter()
admin_module_router = APIRouter()

# --- Public Module Routes ---

@module_router.get("")
async def get_modules(
    type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    modules = ModuleService.get_all_modules(db, type)
    return [m.to_dict() for m in modules]

@module_router.get("/leaderboard")
async def get_global_leaderboard(
    limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    from app.domain.leaderboard_service import LeaderboardService
    rankings = LeaderboardService.get_global_rankings(db, limit)
    return rankings

@module_router.get("/{slug}")
async def get_module_by_slug(
    slug: str,
    db: Session = Depends(get_db)
):
    module = ModuleService.get_module_by_slug(db, slug)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module.to_dict()

@module_router.post("/analytics/start", status_code=201)
async def track_start(
    payload: dict = Body(...), user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = user.id
    module_id = payload.get('module_id')
    
    if not module_id:
        raise HTTPException(status_code=400, detail="module_id required")
        
    try:
        entry = ModuleService.track_module_start(db, user_id, module_id)
        return {"message": "Launch tracked", "entry_id": entry.id}
    except Exception as e:
        if "Session already active" in str(e):
            raise HTTPException(status_code=409, detail="Session already active for this module")
        raise HTTPException(status_code=500, detail="Internal error tracking start")

@module_router.post("/analytics/end")
async def track_end(payload: dict = Body(...), user : User = Depends(get_current_user)):
    user_id  = user.id
    entry_id = payload.get('entry_id')
    duration = payload.get('duration', 0)
    
    if not entry_id:
        raise HTTPException(status_code=400, detail="entry_id required")
        
    try:
        success, message = ModuleService.track_module_end(user_id, entry_id, duration)
        if success:
            return {"message": message}
        raise HTTPException(status_code=404, detail=message)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal error tracking end")

@module_router.post("/execute/{slug}")
async def execute_module(
    slug: str, 
    db: Session = Depends(get_db),
    payload: dict = Body(...), 
    user : User = Depends(get_current_user)
):
    user_id = user.id
    try:
        entry_id = payload.get('entry_id')
        result = LifecycleService.execute_module(db, user_id, slug, payload, entry_id)
        return result
    except KeyError as e:
        raise HTTPException(status_code=404, detail=f"Module Not Found: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

# --- Admin Module Routes ---

@admin_module_router.post("", status_code=201)
async def create_module(
    db: Session = Depends(get_db),
    payload: dict = Body(...), 
    _ = Depends(get_admin_user)
):
    new_module = ModuleService.create_module(db, payload)
    return new_module.to_dict()

@admin_module_router.patch("/{id}")
async def update_module(
    id: int, 
    payload: dict = Body(...), 
    _ = Depends(get_admin_user)
):
    module = ModuleService.update_module(id, payload)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    return module.to_dict()

@admin_module_router.delete("/{id}")
async def delete_module(
    id: int, 
    _ = Depends(get_admin_user)
):
    if ModuleService.delete_module(id):
        return {"message": "Module purged"}
    raise HTTPException(status_code=404, detail="Module not found")

@admin_module_router.post("/seed")
async def seed_modules(_ = Depends(get_admin_user)):
    result = ModuleService.seed_modules()
    return {"message": "Modules seeded successfully", "data": result}

