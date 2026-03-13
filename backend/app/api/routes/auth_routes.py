"""
app/routes/auth_routes.py

Authentication API routes for AppNest.

IMPORTANT:
- This file exposes API-only endpoints (JSON in / JSON out)
- No HTML rendering
- No sessions
- Designed for React frontend + JWT authentication
"""

from flask import Blueprint
from app.controllers.auth_controller import AuthController

# All authentication-related routes are grouped under /api/auth
auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Authenticate an existing user.

    Expected input (JSON):
    {
        "email": "user@example.com",
        "password": "password"
    }

    Response:
    - JWT access token
    - JWT refresh token
    - Basic user info
    """
    return AuthController.login()


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new user.

    Expected input (JSON):
    {
        "email": "user@example.com",
        "password": "password",
        ...
    }

    Response:
    - JWT tokens OR OTP verification requirement
    """
    return AuthController.register()


@auth_bp.route("/verify-otp", methods=["POST"])
def verify_otp():
    """
    Verify OTP sent during registration or password reset.

    Expected input (JSON):
    {
        "email": "user@example.com",
        "otp": "123456"
    }
    """
    return AuthController.verify_otp()


@auth_bp.route("/resend-otp", methods=["POST"])
def resend_otp():
    """
    Resend OTP to user's email.
    """
    return AuthController.resend_otp()


@auth_bp.route("/refresh", methods=["POST"])
def refresh():
    """
    Rotate refresh token and issue new access token.
    """
    return AuthController.refresh()


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """
    Revoke current session.
    """
    return AuthController.logout()


@auth_bp.route("/logout-all", methods=["POST"])
def logout_all():
    """
    Revoke all sessions for current user.
    """
    return AuthController.logout_all()


@auth_bp.route("/me", methods=["GET"])
def me():
    """
    Get current authenticated user info.
    """
    return AuthController.me()


@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    """
    Trigger password reset OTP.
    """
    return AuthController.forgot_password()


@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    """
    Reset password after OTP verification.
    """
    return AuthController.reset_password()
