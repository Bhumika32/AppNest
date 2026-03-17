from fastapi import APIRouter, Depends, HTTPException, Body
from typing import Optional
from app.domain.roast_service import RoastService
from app.platform.module_result import ModuleResult
from app.utils.auth_decorators import get_current_user
roast_router = APIRouter()

@roast_router.get("/normal")
async def get_normal_roast(_: dict = Depends(get_current_user)):
    """Get a normal (friendly) roast."""
    roast = RoastService.get_normal_roast()
    return {"roast": roast, "intensity": "low", "type": "normal"}

@roast_router.post("/personal")
async def get_personal_roast(payload: dict = Body(...), _: dict = Depends(get_current_user)):
    """Get a personalized roast."""
    name = payload.get("name", "Dev")
    roast = RoastService.get_personal_roast(name)
    return {"name": name, "roast": roast, "intensity": "medium", "type": "personal"}

@roast_router.get("/ultra")
async def get_ultra_roast(_: dict = Depends(get_current_user)):
    """Get an ultra (maximum intensity) roast."""
    roast = RoastService.get_ultra_roast()
    return {"roast": roast, "intensity": "high", "type": "ultra"}

@roast_router.get("/game/{game_name}")
async def get_game_roast(game_name: str, _: dict = Depends(get_current_user)):
    """Get a game-specific roast."""
    mock_result = ModuleResult(completed=False, status="lose", score=0)
    roast = RoastService.get_roast(game_name, mock_result)
    return {"roast": roast, "intensity": "medium", "game": game_name, "type": "game"}

@roast_router.get("/tool/{tool_name}")
async def get_tool_roast(tool_name: str, _: dict = Depends(get_current_user)):
    """Get a tool-specific roast."""
    mock_result = ModuleResult(completed=True, status="success", score=0)
    roast = RoastService.get_roast(tool_name, mock_result)
    return {"roast": roast, "intensity": "low", "tool": tool_name, "type": "tool"}

@roast_router.get("/random")
async def get_random_roast(_: dict = Depends(get_current_user)):
    """Get a random roast."""
    roast = RoastService.get_normal_roast()
    return {"roast": roast, "intensity": "medium", "type": "random"}
