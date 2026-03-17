"""
File: app/schemas/profile_schema.py

Profile-related API schemas.
"""

from pydantic import BaseModel
from typing import Optional, List, Dict

# -----------------------------

# PROFILE

# -----------------------------

class ProfileResponse(BaseModel):
    """Basic user profile information."""
id: int
username: str
email: str
first_name: Optional[str]
last_name: Optional[str]
avatar_url: Optional[str]
bio: Optional[str]
joined_date: str

# -----------------------------

# STATISTICS

# -----------------------------

class StatisticsResponse(BaseModel):
    """User profile statistics."""
games_played: int
tools_used: int
total_roasts: int
account_age_days: int
credits: int
performance_history: List[Dict]

# -----------------------------

# FULL PROFILE

# -----------------------------

class FullProfileResponse(BaseModel):
    """Comprehensive profile response with statistics and achievements."""
profile: ProfileResponse
statistics: StatisticsResponse
achievements: List[str]

# -----------------------------

# DASHBOARD

# -----------------------------

class DashboardUser(BaseModel):
    """User information for the dashboard."""
username: str
avatar: Optional[str]
role: str

class DashboardQuest(BaseModel):
    """Daily quest information for the dashboard."""
id: int
task: str
reward: str
progress: int
color: str

class DashboardResponse(BaseModel):
    """Dashboard response containing user and activity information."""
xp: int
level: int
rank: str
title: str
uptime: str
performance_history: List[Dict]
recent_activity: List[Dict]
daily_quests: List[DashboardQuest]
user: DashboardUser
