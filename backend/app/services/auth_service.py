from typing import Tuple, Optional, List
from datetime import datetime, timedelta
from app.core.extensions import db
from app.models.user import User
from app.models.role import Role
from app.models.session import Session
from app.core.security import hash_data, generate_secure_token

class AuthService:
    """
    Service layer for authentication and session lifecycle management.
    """

    @staticmethod
    def register_user(username: str, email: str, password: str) -> Tuple[bool, str, Optional[User]]:
        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            if existing_user.is_verified is False:
                db.session.delete(existing_user)
                db.session.commit()
            else:
                return False, "Username or Email already exists.", None

        # Default role is USER (id=1)
        role = Role.query.filter_by(name="USER").first()
        if not role:
            # Fallback for first run if roles not initialized
            role = Role(name="USER")
            db.session.add(role)
            db.session.commit()

        user = User(
            username=username,
            email=email,
            role_id=role.id,
            is_verified=False
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return True, "Registration successful. Please verify your email.", user

    @staticmethod
    def login_user(email: str, password: str, device_info: str = None, ip_address: str = None) -> Tuple[bool, str, Optional[User], Optional[Session], Optional[str]]:
        """
        Authenticate and create a session.
        Returns: (success, message, user, session, raw_refresh_token)
        """
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return False, "Invalid email or password.", None, None, None

        if not user.is_verified:
            return False, "Please verify your email before login.", None, None, None

        # Create Session
        refresh_token = generate_secure_token()
        hashed_refresh = hash_data(refresh_token)
        
        # Sessions expire in 30 days
        expires_at = datetime.utcnow() + timedelta(days=30)

        session = Session(
            user_id=user.id,
            refresh_token_hash=hashed_refresh,
            device_info=device_info,
            ip_address=ip_address,
            expires_at=expires_at
        )

        db.session.add(session)
        db.session.commit()

        return True, "Login successful.", user, session, refresh_token

    @staticmethod
    def refresh_session(old_refresh_token: str) -> Tuple[bool, str, Optional[User], Optional[Session], Optional[str]]:
        """
        Validate old refresh token and rotate it.
        """
        hashed_old = hash_data(old_refresh_token)
        session = Session.query.filter_by(refresh_token_hash=hashed_old, revoked=False).first()

        if not session or session.is_expired():
            return False, "Invalid or expired session. Please login again.", None, None, None

        # Refresh rotation: generate new token, update session
        new_refresh_token = generate_secure_token()
        session.refresh_token_hash = hash_data(new_refresh_token)
        session.expires_at = datetime.utcnow() + timedelta(days=30) # Slide expiry
        session.last_used_at = datetime.utcnow()

        db.session.commit()

        return True, "Token refreshed.", session.user, session, new_refresh_token

    @staticmethod
    def logout_session(refresh_token: str) -> bool:
        """Revoke a specific session."""
        hashed_token = hash_data(refresh_token)
        session = Session.query.filter_by(refresh_token_hash=hashed_token).first()
        if session:
            session.revoked = True
            db.session.commit()
            return True
        return False

    @staticmethod
    def logout_all_sessions(user_id: int) -> int:
        """Revoke all active sessions for a user."""
        count = Session.query.filter_by(user_id=user_id, revoked=False).update({"revoked": True})
        db.session.commit()
        return count

    @staticmethod
    def verify_user(email: str) -> bool:
        """Mark a user as verified."""
        user = User.query.filter_by(email=email).first()
        if user:
            user.is_verified = True
            db.session.commit()
            return True
        return False

    @staticmethod
    def reset_password(email: str, new_password: str) -> bool:
        """Update password and revoke all existing sessions."""
        user = User.query.filter_by(email=email).first()
        if user:
            user.set_password(new_password)
            db.session.commit()
            AuthService.logout_all_sessions(user.id)
            return True
        return False
