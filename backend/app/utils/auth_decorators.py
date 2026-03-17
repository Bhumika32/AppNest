"""
app/utils/auth_decorators.py
FastAPI Auth Dependencies (NO decorators, pure DI)
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.jwt_manager import JWTManager
from app.core.database import get_db
from app.models import User

security = HTTPBearer()


# -----------------------------
# TOKEN VALIDATION
# -----------------------------
def get_token_payload(
    auth: HTTPAuthorizationCredentials = Depends(security)
):
    payload = JWTManager.validate_token(auth.credentials)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return payload


# -----------------------------
# CURRENT USER
# -----------------------------
def get_current_user(
    payload: dict = Depends(get_token_payload),
    db: Session = Depends(get_db)
) -> User:

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    user = db.get(User, int(user_id))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


# -----------------------------
# ROLE CHECK (GENERIC)
# -----------------------------
def require_role(required_role: str):

    def role_checker(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
        if not user.role or user.role.name.lower() != required_role.lower():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"{required_role} access required",
            )

        return user

    return role_checker


# -----------------------------
# PREDEFINED ROLES
# -----------------------------
def get_admin_user(user: User = Depends(require_role("admin"))):
    return user


def get_user_user(user: User = Depends(require_role("user"))):
    return user

# """
# app/utils/auth_decorators.py

# Authentication and Authorization dependencies for FastAPI.
# """

# from fastapi import Depends, HTTPException, status
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from app.core.jwt_manager import JWTManager
# from app.models import User
# from app.core.database import get_db
# from sqlalchemy.orm import Session

# security = HTTPBearer()

# async def get_current_user_claims(auth: HTTPAuthorizationCredentials = Depends(security)):
#     """FastAPI dependency to verify JWT and return payload."""
#     payload = JWTManager.validate_token(auth.credentials)
#     if not payload:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid or expired token",
#         )
#     return payload


# async def get_current_user(
#     claims: dict = Depends(get_current_user_claims),
#     db: Session = Depends(get_db)
# ) -> User:
#     """Return the authenticated user."""

#     user_id = claims.get("sub")

#     if not user_id:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="User ID not found in token",
#         )

#     user = db.get(User, int(user_id))

#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="User not found",
#         )

#     return user

# async def get_admin_user(user: User = Depends(get_current_user)) -> User:
#     """FastAPI dependency to verify user has admin role."""
#     if not user.role or user.role.name.lower() != 'admin':
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Admin access required",
#         )
#     return user

