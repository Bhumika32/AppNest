"""
File: app/schemas/module_schema.py

Module + leaderboard schemas.
"""

from pydantic import BaseModel
from typing import List, Optional

class ModuleResponse(BaseModel):
    """Basic module information."""
id: int
name: str
slug: str
type: str
is_active: bool

class ModuleListResponse(BaseModel):
    """Response for listing modules."""
modules: List[ModuleResponse]

# -----------------------------

# LEADERBOARD

# -----------------------------

class LeaderboardEntry(BaseModel):
    """Leaderboard entry for a user."""
username: str
total_xp: int
level: int

class LeaderboardResponse(BaseModel):
    """Response for the leaderboard."""
rankings: List[LeaderboardEntry]

# -----------------------------

# ANALYTICS TRACKING

# -----------------------------

class StartTrackingResponse(BaseModel):
    """Response for starting tracking."""
message: str
entry_id: int

class SimpleMessageResponse(BaseModel):
    """Simple message response."""
message: str
