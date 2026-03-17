"""app.core.jwt_manager
A custom JWT management class using PyJWT, providing token issuance and validation."""
import jwt
# import os
from datetime import datetime, timedelta
from app.core.config import settings

import jwt
from datetime import datetime, timedelta
from app.core.config import settings


class JWTManager:
    """Custom JWT management using PyJWT."""

    ALGORITHM = "HS256"

    @staticmethod
    def issue_access_token(user_id, role, session_id):
        expire = datetime.utcnow() + timedelta(
            seconds=settings.JWT_ACCESS_TOKEN_EXPIRES
        )

        payload = {
            "sub": str(user_id),
            "role": (role or "user").lower(),
            "session_id": session_id,
            "exp": expire,
            "iat": datetime.utcnow()
        }

        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=JWTManager.ALGORITHM)

    @staticmethod
    def validate_token(token: str):
        """
        Validate and decode JWT token
        """
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[JWTManager.ALGORITHM]
            )
            return payload

        except jwt.ExpiredSignatureError:
            return None

        except jwt.InvalidTokenError:
            return None
