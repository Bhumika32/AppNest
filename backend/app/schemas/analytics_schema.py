"""
File: app/schemas/analytics_schema.py

Admin analytics schemas.
"""

from pydantic import BaseModel
from typing import List

class PlatformStatsResponse(BaseModel):
    """Key platform statistics for admin dashboard."""
    activeUsers: int
    matchesToday: int
    toolUsage: int
    roastBattles: int
    systemHealth: str
    growthTrend: float

class UserGrowthItem(BaseModel):
    """User growth data for a specific date."""
    date: str
    users: int
    newUsers: int

class GameAnalyticsItem(BaseModel):
    """Game analytics data."""
    name: str
    sessions: int

class ToolAnalyticsItem(BaseModel):
    """Tool analytics data."""
    name: str
    sessions: int

class UserGrowthResponse(BaseModel):
    """Response for user growth analytics."""
    data: List[UserGrowthItem]

class GameAnalyticsResponse(BaseModel):
    """Response for game analytics."""
    data: List[GameAnalyticsItem]

class ToolAnalyticsResponse(BaseModel):
    """Response for tool analytics."""
    data: List[ToolAnalyticsItem]
