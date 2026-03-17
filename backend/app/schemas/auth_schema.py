"""
File: app/schemas/auth_schema.py

Auth response schemas.
"""

from pydantic import BaseModel
from typing import Optional

class UserResponse(BaseModel):
    """Basic user information for auth responses."""
id: int
email: str
username: str
role: str
avatar_url: Optional[str]
is_verified: bool

class LoginResponse(BaseModel):
    """Response for login requests."""
access_token: str
user: UserResponse

class TokenResponse(BaseModel):
    """Response for token refresh requests."""
access_token: str

class MessageResponse(BaseModel):
    """Simple message response."""
message: str
