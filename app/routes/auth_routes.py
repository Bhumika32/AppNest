"""
app/routes/auth_routes.py

Authentication routes for AppNest:
- Login
- Register
- OTP verification
- Resend OTP
- Logout
"""

from flask import Blueprint
from app.controllers.auth_controller import AuthController

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    return AuthController.login()


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    return AuthController.register()


@auth_bp.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():
    return AuthController.verify_otp()


@auth_bp.route("/resend-otp", methods=["POST"])
def resend_otp():
    return AuthController.resend_otp()

@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    return AuthController.forgot_password()


@auth_bp.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    return AuthController.reset_password()

@auth_bp.route("/logout", methods=["GET"])
def logout():
    return AuthController.logout()