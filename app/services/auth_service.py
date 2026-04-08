"""
app/services/auth_service.py

Auth service layer:
- User registration (creates unverified account first)
- User login (only allowed if verified)
- Mark user as verified after OTP success
"""

from app.extensions import db
from app.models.user import User


class AuthService:
    """Service layer for authentication DB operations."""

    @staticmethod
    def register_user(username: str, email: str, password: str) -> tuple[bool, str, User | None]:
        """
        Register a new user in an unverified state.
        OTP verification must be completed to activate the account.

        Returns:
            (success, message, user)
        """
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            # If user exists but not verified, allow re-registration by deleting old record
            if existing_user.is_verified is False:
                db.session.delete(existing_user)
                db.session.commit()
            else:
                return False, "Username or Email already exists.", None

        user = User(username=username, email=email, is_verified=False)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return True, "Registration started. OTP sent to your email.", user

    @staticmethod
    def verify_user_email(user_id: int) -> tuple[bool, str]:
        """
        Mark user as verified after successful OTP verification.
        """
        user = User.query.get(user_id)
        if not user:
            return False, "User not found."

        user.is_verified = True
        db.session.commit()

        return True, "Email verified successfully. You can now login."

    @staticmethod
    def login_user(username: str, password: str) -> tuple[bool, str, User | None]:
        """
        Authenticate user credentials.
        Only verified users are allowed to login.
        """
        user = User.query.filter_by(username=username).first()

        if not user:
            return False, "User not found.", None

        if not user.is_verified:
            return False, "Please verify your email before login.", None

        if not user.check_password(password):
            return False, "Invalid password.", None

        return True, "Login successful.", user