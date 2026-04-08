"""
app/api/deps/auth.py

Production-grade FastAPI Auth Dependencies
- Stateless
- Secure
- Strict validation
- No data leakage
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import logging

from app.core.jwt_manager import JWTManager
from app.core.database import get_db
from app.models import User, Session as UserSession

logger = logging.getLogger(__name__)

security = HTTPBearer(auto_error=True)


# -----------------------------------------------------
# TOKEN PAYLOAD
# -----------------------------------------------------
def get_token_payload(
    auth: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Extract and validate JWT token payload
    """
    token = auth.credentials

    payload = JWTManager.validate_token(token)

    if not payload:
        logger.warning("Invalid or expired JWT token used")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    return payload


# -----------------------------------------------------
# CURRENT USER (CORE DEPENDENCY)
# -----------------------------------------------------
def get_current_user(
    payload: dict = Depends(get_token_payload),
    db: Session = Depends(get_db)
) -> User:
    """
    Resolve current authenticated user from JWT + session validation
    """

    # ---- STRICT PAYLOAD VALIDATION ----
    try:
        user_id = int(payload["sub"])
        session_id = str(payload["session_id"])
    except (KeyError, ValueError, TypeError):
        logger.warning("Malformed JWT payload")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    # ---- SESSION VALIDATION ----
    session = db.get(UserSession, session_id)

    if not session:
        logger.warning(f"Session not found: {session_id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    if session.revoked:
        logger.warning(f"Revoked session access attempt: {session_id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    if session.is_expired():
        logger.warning(f"Expired session access attempt: {session_id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    # ---- USER VALIDATION ----
    user = db.get(User, user_id)

    if not user:
        logger.warning(f"User not found for token: {user_id}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    return user


# -----------------------------------------------------
# ROLE CHECK (GENERIC)
# -----------------------------------------------------
def require_role(required_role: str):
    """
    Role-based access control dependency
    """

    def role_checker(
        user: User = Depends(get_current_user)
    ) -> User:

        # Defensive: ensure role exists
        if not user.role or not user.role.name:
            logger.warning(f"User {user.id} has no role assigned")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied",
            )

        if user.role.name.lower() != required_role.lower():
            logger.warning(
                f"Unauthorized role access: user={user.id}, role={user.role.name}, required={required_role}"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied",
            )

        return user

    return role_checker


# -----------------------------------------------------
# PREDEFINED ROLE DEPENDENCIES
# -----------------------------------------------------
def get_admin_user(user: User = Depends(require_role("admin"))) -> User:
    return user


def get_user_user(user: User = Depends(require_role("user"))) -> User:
    return user