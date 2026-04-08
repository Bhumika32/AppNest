# -----------------------------------------------------------------------------
# PRODUCTION AUTH SERVICE (SECURE + CONSISTENT + ROTATION SAFE)
# -----------------------------------------------------------------------------

import hmac
import hashlib
import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session as DBSession

from app.models.user import User
from app.core.security import generate_secure_token
from app.repositories.user_repository import user_repository
from app.repositories.session_repository import session_repository

logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# HELPERS
# -----------------------------------------------------------------------------
def hash_token(token: str) -> str:
    """
    Securely hash refresh token before storing in DB
    """
    return hashlib.sha256(token.encode()).hexdigest()


# -----------------------------------------------------------------------------
# AUTH SERVICE
# -----------------------------------------------------------------------------
class AuthService:

    # -------------------------------------------------------------------------
    # LOGIN
    # -------------------------------------------------------------------------
    @staticmethod
    def login_user(
        db: DBSession,
        email: str,
        password: str,
        device_info: str = None,
        ip_address: str = None
    ):
        try:
            email = email.lower().strip()

            user = user_repository.get_active_user_by_email(db, email)

            if not user or not user.check_password(password):
                return False, "Invalid credentials", None, None, None

            if not user.is_active:
                return False, "Account disabled", None, None, None

            if not user.is_verified:
                return False, "Email not verified", None, None, None

            # -----------------------------------------------------------------
            # SESSION POLICY (single session)
            # -----------------------------------------------------------------
            session_repository.revoke_active_sessions(db, user.id)

            # -----------------------------------------------------------------
            # TOKEN GENERATION
            # -----------------------------------------------------------------
            raw_token = generate_secure_token()
            hashed_token = hash_token(raw_token)

            # -----------------------------------------------------------------
            # CREATE SESSION
            # -----------------------------------------------------------------
            session = session_repository.create(db, {
                "user_id": user.id,
                "refresh_token_hash": hashed_token,
                "device_info": device_info,
                "ip_address": ip_address,
                "expires_at": datetime.utcnow() + timedelta(days=30),
                "revoked": False,
                "last_used_at": datetime.utcnow()
            })

            db.commit()
            db.refresh(session)

            # -----------------------------------------------------------------
            # UPDATE USER LAST LOGIN
            # -----------------------------------------------------------------
            user_repository.update(db, user, {
                "last_login_at": datetime.utcnow()
            })

            db.commit()

            return True, "Login successful", user, session, raw_token

        except Exception:
            db.rollback()
            logger.exception("Login error")
            return False, "Login failed", None, None, None

    # -------------------------------------------------------------------------
    # REFRESH
    # -------------------------------------------------------------------------
    @staticmethod
    def refresh_session(
        db: DBSession,
        session_id: str,
        provided_token: str
    ):
        try:
            session = session_repository.get_by_id(db, session_id)

            if not session:
                return False, "Session not found", None, None, None

            if session.revoked or session.is_expired():
                return False, "Session expired", None, None, None

            # -----------------------------------------------------------------
            # HASH PROVIDED TOKEN
            # -----------------------------------------------------------------
            hashed_provided = hash_token(provided_token)

            # -----------------------------------------------------------------
            # TOKEN VALIDATION
            # -----------------------------------------------------------------
            if not hmac.compare_digest(
                hashed_provided,
                session.refresh_token_hash
            ):
                # 🔥 REUSE DETECTION (CRITICAL SECURITY FEATURE)
                logger.warning(
                    f"[TOKEN REUSE DETECTED] session={session.id}, user={session.user_id}"
                )

                session_repository.update(db, session, {
                    "revoked": True
                })
                db.commit()

                return False, "Invalid token", None, None, None

            # -----------------------------------------------------------------
            # ROTATE TOKEN
            # -----------------------------------------------------------------
            new_raw_token = generate_secure_token()
            new_hashed_token = hash_token(new_raw_token)

            session_repository.update(db, session, {
                "refresh_token_hash": new_hashed_token,
                "last_used_at": datetime.utcnow(),
                "expires_at": datetime.utcnow() + timedelta(days=30)
            })

            db.commit()
            db.refresh(session)

            return True, "Refreshed", session.user, session, new_raw_token

        except Exception:
            db.rollback()
            logger.exception("Refresh error")
            return False, "Refresh failed", None, None, None

    # -------------------------------------------------------------------------
    # LOGOUT
    # -------------------------------------------------------------------------
    @staticmethod
    def logout_session(db: DBSession, session_id: str):
        try:
            session = session_repository.get_by_id(db, session_id)

            if not session:
                return False

            session_repository.update(db, session, {
                "revoked": True
            })

            db.commit()
            return True

        except Exception:
            db.rollback()
            logger.exception("Logout error")
            return False
# import hmac n
# from typing import Tuple, Optional
# from datetime import datetime, timedelta
# import logging
# import hmac
# from sqlalchemy.orm import Session as DBSession

# from app.models.user import User
# from app.models.session import Session as UserSession
# from app.core.security import hash_data, generate_secure_token
# from app.repositories.user_repository import user_repository
# from app.repositories.role_repository import role_repository
# from app.repositories.session_repository import session_repository

# logger = logging.getLogger(__name__)

# class AuthService:

#     @staticmethod
#     def register_user(db: DBSession, username: str, email: str, password: str):
#         try:
#             email = email.lower().strip()
            
#             existing_user = user_repository.get_by_email_or_username(db, email, username)

#             if existing_user:
#                 if not existing_user.is_verified:
#                     user_repository.delete(db, existing_user.id)
#                 else:
#                     return False, "Username or Email already exists.", None

#             role = role_repository.get_by_name(db, "user")
#             if not role:
#                 role = role_repository.create(db, {"name": "user"})

#             user_in = {
#                 "username": username.strip(),
#                 "email": email,
#                 "role_id": role.id,
#                 "is_verified": False,
#                 "is_active": True
#             }

#             user = User(**user_in)
#             user.set_password(password)
#             db.add(user)
#             db.commit()
#             db.refresh(user)

#             logger.info(f"User registered: {email}")
#             return True, "Registration successful. Verify your email.", user

#         except Exception as e:
#             db.rollback()
#             logger.exception("Register error")
#             return False, "Registration failed.", None

#     @staticmethod
#     def login_user(db: DBSession, email: str, password: str, device_info: str = None, ip_address: str = None):
#         try:
#             email = email.lower().strip()
#             user = user_repository.get_active_user_by_email(db, email)

#             if not user or not user.check_password(password):
#                 return False, "Invalid credentials", None, None, None

#             if not user.is_active:
#                 return False, "Account disabled", None, None, None

#             if not user.is_verified:
#                 return False, "Email not verified", None, None, None

#             session_repository.revoke_active_sessions(db, user.id)

#             refresh_token = generate_secure_token()
#             hashed_refresh =refresh_token

#             session_in = {
#                 "user_id": user.id,
#                 "refresh_token_hash": hashed_refresh,
#                 "device_info": device_info,
#                 "ip_address": ip_address,
#                 "expires_at": datetime.utcnow() + timedelta(days=30),
#                 "revoked": False,
#                 "last_used_at": datetime.utcnow()
#             }
#             session = session_repository.create(db, session_in)

#             db.add(session)
#             db.commit()
#             db.refresh(session)
#             if not session:
#                 return Exception("Session creation failed")

#             user_repository.update(db, user, {"last_login_at": datetime.utcnow()})

#             logger.info(f"User login: {email}")
#             return True, "Login successful", user, session, refresh_token

#         except Exception:
#             db.rollback()
#             logger.exception("Login error")
#             return False, "Login failed", None, None, None

#     @staticmethod
#     def refresh_session(db: DBSession, session_id: str, provided_token: str):
#         try:
#             session = session_repository.get_by_id(db, session_id)

#             if not session:
#                 return False, "Session not found", None, None, None

#             if session.revoked or session.is_expired():
#                 return False, "Session expired", None, None, None

#             if not hmac.compare_digest(provided_token, session.refresh_token_hash):
#                 logger.warning("Token reuse detected")
#                 return False, "Invalid token", None, None, None

#             new_token = generate_secure_token()

#             session_repository.update(db, session, {
#                 "refresh_token_hash": new_token,   # ✅ FIXED
#                 "last_used_at": datetime.utcnow(),
#                 "expires_at": datetime.utcnow() + timedelta(days=30)
#             })

#             return True, "Refreshed", session.user, session, new_token

#         except Exception:
#             db.rollback()
#             logger.exception("Refresh error")
#             return False, "Refresh failed", None, None, None

#     @staticmethod
#     def logout_session(db: DBSession, session_id: str):
#         try:
#             session = session_repository.get_by_id(db, session_id)
#             if not session:
#                 return False

#             session_repository.update(db, session, {"revoked": True})
#             return True

#         except Exception:
#             db.rollback()
#             logger.exception("Logout error")
#             return False

#     @staticmethod
#     def verify_user(db: DBSession, email: str):
#         try:
#             user = user_repository.get_by_email(db, email)
#             if not user:
#                 return False

#             user_repository.update(db, user, {"is_verified": True})
#             logger.info(f"User verified: {email}")
#             return True

#         except Exception:
#             db.rollback()
#             logger.exception("Verify error")
#             return False

#     @staticmethod
#     def reset_password(db: DBSession, email: str, new_password: str):
#         try:
#             user = user_repository.get_by_email(db, email)
#             if not user:
#                 return False

#             user.set_password(new_password)
#             db.commit()

#             session_repository.revoke_all_sessions(db, user.id)

#             logger.info(f"Password reset: {email}")
#             return True

#         except Exception:
#             db.rollback()
#             logger.exception("Reset error")
#             return False
