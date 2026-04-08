from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.roast_service import RoastService
from app.platform.module_result import ModuleResult
from app.api.deps.auth import get_current_user
from app.models.user import User

roast_router = APIRouter()

@roast_router.get("/normal")
async def get_normal_roast(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a normal (friendly) roast."""
    roast = RoastService.get_normal_roast()
    return {"roast": roast, "intensity": "low", "type": "normal"}

@roast_router.post("/personal")
async def get_personal_roast(
    payload: dict = Body(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a personalized roast."""
    name = payload.get("name", user.username if user.username else "Dev")
    roast = RoastService.get_personal_roast(name)
    return {"name": name, "roast": roast, "intensity": "medium", "type": "personal"}

@roast_router.get("/ultra")
async def get_ultra_roast(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get an ultra (maximum intensity) roast."""
    roast = RoastService.get_ultra_roast()
    return {"roast": roast, "intensity": "high", "type": "ultra"}

@roast_router.get("/game/{game_name}")
async def get_game_roast(
    game_name: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a game-specific roast."""
    mock_result = ModuleResult(completed=False, status="lose", score=0)
    roast = RoastService.get_roast(game_name, mock_result)
    return {"roast": roast, "intensity": "medium", "game": game_name, "type": "game"}

@roast_router.get("/tool/{tool_name}")
async def get_tool_roast(
    tool_name: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a tool-specific roast."""
    mock_result = ModuleResult(completed=True, status="success", score=0)
    roast = RoastService.get_roast(tool_name, mock_result)
    return {"roast": roast, "intensity": "low", "tool": tool_name, "type": "tool"}

@roast_router.get("/random")
async def get_random_roast(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a random roast."""
    roast = RoastService.get_normal_roast()
    return {"roast": roast, "intensity": "medium", "type": "random"}
