# File: app/schemas/module_schema.py

from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# -----------------------------
# MODULE
# -----------------------------

class ModuleResponse(BaseModel):
    id: int
    name: str
    slug: str
    component_key: str
    type: str
    is_active: bool
    description: Optional[str] = None,
    capabilities: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True


class ModuleListResponse(BaseModel):
    modules: List[ModuleResponse]


# -----------------------------
# GLOBAL LEADERBOARD
# -----------------------------

class GlobalLeaderboardEntry(BaseModel):
    username: str
    total_xp: int
    level: int
    rank: int


class GlobalLeaderboardResponse(BaseModel):
    rankings: List[GlobalLeaderboardEntry]


# -----------------------------
# MODULE LEADERBOARD
# -----------------------------

class ModuleLeaderboardEntry(BaseModel):
    username: str
    top_score: int
    rank: int


class ModuleLeaderboardResponse(BaseModel):
    rankings: List[ModuleLeaderboardEntry]


# -----------------------------
# ANALYTICS TRACKING
# -----------------------------

class StartTrackingResponse(BaseModel):
    message: str
    entry_id: int


class SimpleMessageResponse(BaseModel):
    message: str
    