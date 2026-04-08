"""
app/core/jwt_manager.py

Production-grade JWT Manager
- Strict validation
- Token type enforcement
- Issuer & audience validation
- Logging for observability
"""

import jwt
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from requests import Session

from app.core.config import settings

logger = logging.getLogger(__name__)


class JWTManager:
    """
    Secure JWT Manager using PyJWT
    """

    ALGORITHM = "HS256"
    ISSUER = "appnest"
    AUDIENCE = "appnest_users"

    # -----------------------------------------------------
    # ISSUE ACCESS TOKEN
    # -----------------------------------------------------
    @staticmethod
    def issue_access_token(
        user_id: int,
        role: str,
        session_id: str
    ) -> str:
        """
        Generate a secure access token
        """

        expire = datetime.utcnow() + timedelta(
            seconds=settings.JWT_ACCESS_TOKEN_EXPIRES
        )

        payload = {
            "sub": str(user_id),
            "role": (role or "user").lower(),
            "session_id": str(session_id),
            "type": "access",
            "iss": JWTManager.ISSUER,
            "aud": JWTManager.AUDIENCE,
            "exp": expire,
            "iat": datetime.utcnow(),
        }

        try:
            token = jwt.encode(
                payload,
                settings.JWT_SECRET_KEY,
                algorithm=JWTManager.ALGORITHM
            )
            return token

        except Exception as e:
            logger.error(f"JWT encoding failed: {str(e)}")
            raise


    # -----------------------------------------------------
    # VALIDATE TOKEN
    # -----------------------------------------------------
    @staticmethod
    def validate_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Validate and decode JWT token securely
        """

        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[JWTManager.ALGORITHM],
                audience=JWTManager.AUDIENCE,
                issuer=JWTManager.ISSUER,
            )

            # ---- TYPE VALIDATION ----
            if payload.get("type") != "access":
                logger.warning("Invalid token type used")
                return None

            return payload

        except jwt.ExpiredSignatureError:
            logger.warning("Expired JWT token used")

        except jwt.InvalidAudienceError:
            logger.warning("Invalid JWT audience")

        except jwt.InvalidIssuerError:
            logger.warning("Invalid JWT issuer")

        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid JWT token: {str(e)}")

        except Exception as e:
            logger.error(f"Unexpected JWT validation error: {str(e)}")

        return None