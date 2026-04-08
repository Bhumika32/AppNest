"""
File: app/schemas/auth_schema.py

Auth response schemas.
"""

from pydantic import BaseModel, EmailStr
from typing import Optional

# -----------------------------------------------------
# Pydantic Request Schemas
# -----------------------------------------------------

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str


class OTPVerifyRequest(BaseModel):
    email: EmailStr
    otp: str


class ResendOTPRequest(BaseModel):
    email: EmailStr


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str

# -----------------------------------------------------
# Pydantic Response Schemas

class UserResponse(BaseModel):
    id: int
    username: Optional[str]
    email: EmailStr
    role: Optional[str]
    avatar_url: Optional[str]
    is_verified: bool

    class Config:
        from_attributes = True

class LoginResponse(BaseModel):
    user: UserResponse
    access_token: str

class OTPResponse(BaseModel):
    message: str

class TokenResponse(BaseModel):
    access_token: str

class MessageResponse(BaseModel):
    message: str

__all__ = [
    'LoginRequest',
    'RegisterRequest',
    'OTPVerifyRequest',
    'ResendOTPRequest',
    'ForgotPasswordRequest',
    'ResetPasswordRequest'
]

