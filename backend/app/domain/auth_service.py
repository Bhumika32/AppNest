"""
Auth Service

Handles:
- User registration
- Login
- Refresh token rotation
- Session lifecycle
- Password reset
- Email verification

Security features implemented:
- Hashed refresh tokens
- Token rotation
- Token reuse detection
- Session revocation
"""

from typing import Tuple, Optional
from datetime import datetime, timedelta

from sqlalchemy.orm import Session as DBSession

from sqlalchemy.orm import Session as DBSession
from app.models.user import User
from app.models.role import Role
from app.models.session import Session as UserSession
from app.core.security import hash_data, generate_secure_token


class AuthService:
    """
    Service layer for authentication and session lifecycle management.

    Responsibilities:
    - Manage user authentication
    - Handle refresh tokens
    - Maintain session lifecycle
    - Enforce security policies
    """

    # -------------------------------------------------------------------------
    # USER REGISTRATION
    # -------------------------------------------------------------------------
    @staticmethod
    def register_user(
        db: DBSession,
        username: str,
        email: str,
        password: str
    ) -> Tuple[bool, str, Optional[User]]:
        """
        Register a new user.

        Returns:
            success (bool)
            message (str)
            created_user (User | None)
        """

        # Check if username or email already exists
        existing_user = db.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            # If user exists but email not verified, remove stale account
            if existing_user.is_verified is False:
                db.delete(existing_user)
                db.commit()
            else:
                return False, "Username or Email already exists.", None

        # Default role assignment
        role = db.query(Role).filter_by(name="USER").first()

        # If role table not initialized yet
        if not role:
            role = Role(name="USER")
            db.add(role)
            db.commit()

        # Create user instance
        user = User(
            username=username,
            email=email,
            role_id=role.id,
            is_verified=False
        )

        # Hash password using model method
        user.set_password(password)

        db.add(user)
        db.commit()

        return True, "Registration successful. Please verify your email.", user

    # -------------------------------------------------------------------------
    # USER LOGIN
    # -------------------------------------------------------------------------
    @staticmethod
    def login_user(
        db: DBSession,
        email: str,
        password: str,
        device_info: str = None,
        ip_address: str = None
    ) -> Tuple[bool, str, Optional[User], Optional[UserSession], Optional[str]]:
        """
        Authenticate a user and create a new session.

        Returns:
            success
            message
            user
            session
            raw_refresh_token
        """

        user = db.query(User).filter_by(email=email).first()

        if not user or not user.check_password(password):
            return False, "Invalid email or password.", None, None, None

        if not user.is_verified:
            return False, "Please verify your email before login.", None, None, None

        # Generate secure refresh token
        refresh_token = generate_secure_token()

        # Store only hashed version in DB
        hashed_refresh = hash_data(refresh_token)

        # Sessions expire in 30 days
        expires_at = datetime.utcnow() + timedelta(days=30)

        session = UserSession(
            user_id=user.id,
            refresh_token_hash=hashed_refresh,
            device_info=device_info,
            ip_address=ip_address,
            expires_at=expires_at
        )

        db.add(session)
        db.commit()

        return True, "Login successful.", user, session, refresh_token

    # -------------------------------------------------------------------------
    # TOKEN REFRESH
    # -------------------------------------------------------------------------
    @staticmethod
    def refresh_session(
        db: DBSession,
        session_id: str,
        provided_token: str
    ) -> Tuple[bool, str, Optional[User], Optional[UserSession], Optional[str]]:
        """
        Validate refresh token and rotate it.

        Security Feature:
        Implements **Token Reuse Detection**

        If a reused token is detected:
            - Assume token theft
            - Revoke ALL sessions for that user
        """

        session = db.query(UserSession).filter_by(id=session_id).first()

        if not session:
            return False, "Session not found.", None, None, None

        if session.revoked or session.is_expired():
            return False, "Session revoked or expired.", None, None, None

        hashed_provided = hash_data(provided_token)

        # ------------------------------------------------------------------
        # TOKEN REUSE DETECTION
        # ------------------------------------------------------------------
        if session.refresh_token_hash != hashed_provided:

            # Possible token theft
            db.query(UserSession).filter_by(
                user_id=session.user_id
            ).update({"revoked": True})

            db.commit()

            return False, "Security Alert: Token reuse detected. All sessions revoked.", None, None, None

        # ------------------------------------------------------------------
        # TOKEN ROTATION
        # ------------------------------------------------------------------
        new_refresh_token = generate_secure_token()

        session.refresh_token_hash = hash_data(new_refresh_token)
        session.last_used_at = datetime.utcnow()

        # Sliding expiration (keeps session alive if user is active)
        session.expires_at = datetime.utcnow() + timedelta(days=30)

        db.commit()

        return True, "Token rotated.", session.user, session, new_refresh_token

    # -------------------------------------------------------------------------
    # LOGOUT CURRENT SESSION
    # -------------------------------------------------------------------------
    @staticmethod
    def logout_session(
        db: DBSession, session_id: str) -> bool:
        """
        Revoke a specific session.
        """

        session = db.query(UserSession).filter_by(id=session_id).first()

        if session:
            session.revoked = True
            db.commit()
            return True

        return False

    # -------------------------------------------------------------------------
    # LOGOUT ALL SESSIONS
    # -------------------------------------------------------------------------
    @staticmethod
    def logout_all_sessions(
        db: DBSession, user_id: int) -> int:
        """
        Revoke all active sessions for a user.
        """

        count = db.query(UserSession).filter_by(
            user_id=user_id,
            revoked=False
        ).update({"revoked": True})

        db.commit()

        return count

    # -------------------------------------------------------------------------
    # EMAIL VERIFICATION
    # -------------------------------------------------------------------------
    @staticmethod
    def verify_user(
        db: DBSession, email: str) -> bool:
        """
        Mark user as verified after email verification.
        """

        user = db.query(User).filter_by(email=email).first()

        if user:
            user.is_verified = True
            db.commit()
            return True

        return False

    # -------------------------------------------------------------------------
    # PASSWORD RESET
    # -------------------------------------------------------------------------
    @staticmethod
    def reset_password(
        db: DBSession, email: str, new_password: str) -> bool:
        """
        Reset user password.

        Security:
        All sessions are revoked after password reset.
        """

        user = db.query(User).filter_by(email=email).first()

        if user:
            user.set_password(new_password)

            db.commit()

            # Revoke all active sessions
            AuthService.logout_all_sessions(db, user.id)

            return True

        return False