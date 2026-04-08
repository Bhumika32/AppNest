import secrets
from datetime import datetime, timedelta
from typing import Tuple
import logging
from sqlalchemy.orm import Session

from app.repositories.otp_repository import otp_repository
from app.repositories.user_repository import user_repository
from app.core.security import hash_data, verify_hash

logger = logging.getLogger(__name__)

class OTPService:

    OTP_LENGTH = 6
    OTP_EXPIRY_MINUTES = 10
    OTP_RESEND_COOLDOWN_SECONDS = 60
    MAX_DAILY_OTPS = 5
    MAX_FAILED_ATTEMPTS = 3

    @staticmethod
    def _utc_now() -> datetime:
        return datetime.utcnow()

    @staticmethod
    def generate_otp(length: int = OTP_LENGTH) -> str:
        return "".join(str(secrets.randbelow(10)) for _ in range(length))

    @staticmethod
    def create_and_store_otp(db: Session, email: str, purpose: str) -> str:
        try:
            email = email.lower().strip()
            user = user_repository.get_by_email_for_update(db, email)

            if not user:
                raise ValueError("User not found")

            now = OTPService._utc_now()
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

            daily_count = otp_repository.get_daily_count(db, user.id, purpose, today_start)
            if daily_count >= OTPService.MAX_DAILY_OTPS:
                raise ValueError("Daily OTP limit reached")

            otp_repository.invalidate_active_tokens(db, user.id, purpose)

            otp = OTPService.generate_otp()
            hashed = hash_data(otp)
            expires_at = now + timedelta(minutes=OTPService.OTP_EXPIRY_MINUTES)

            otp_in = {
                "user_id": user.id,
                "otp_hash": hashed,
                "purpose": purpose,
                "expires_at": expires_at,
                "attempts": 0
            }
            otp_repository.create(db, otp_in)

            logger.info(f"OTP created for {email} ({purpose})")
            return otp

        except Exception as e:
            db.rollback()
            logger.exception("OTP creation failed")
            raise e

    @staticmethod
    def can_resend(db: Session, email: str, purpose: str) -> Tuple[bool, str]:
        email = email.lower().strip()
        user = user_repository.get_active_user_by_email(db, email)

        if not user:
            return False, "User not found"

        latest = otp_repository.get_latest_token(db, user.id, purpose)

        if latest:
            diff = (OTPService._utc_now() - latest.created_at).total_seconds()
            if diff < OTPService.OTP_RESEND_COOLDOWN_SECONDS:
                wait = int(OTPService.OTP_RESEND_COOLDOWN_SECONDS - diff)
                return False, f"Wait {wait}s before resend"

        return True, "Allowed"

    @staticmethod
    def verify_otp(db: Session, email: str, submitted_otp: str, purpose: str) -> Tuple[bool, str]:
        try:
            email = email.lower().strip()
            user = user_repository.get_active_user_by_email(db, email)

            if not user:
                return False, "User not found"

            token = otp_repository.get_active_token_for_update(db, user.id, purpose)

            if not token:
                return False, "No active OTP"

            now = OTPService._utc_now()

            if token.expires_at < now:
                otp_repository.update(db, token, {"used": True})
                return False, "OTP expired"

            if token.attempts >= OTPService.MAX_FAILED_ATTEMPTS:
                otp_repository.update(db, token, {"used": True})
                return False, "Too many attempts"

            if not verify_hash(submitted_otp, token.otp_hash):
                otp_repository.update(db, token, {"attempts": token.attempts + 1})
                return False, "Invalid OTP"

            otp_repository.update(db, token, {"used": True})
            logger.info(f"OTP verified for {email}")
            return True, "OTP verified"

        except Exception as e:
            db.rollback()
            logger.exception("OTP verification failed")
            return False, "Internal error"

    @staticmethod
    def send_otp_email(to_email: str, otp: str, purpose: str = "Verification") -> None:
        """
        Sends an email async. In a real environment, this connects to SMTP/SendGrid.
        """
        import time
        import random
        
        # Simulate network delay for real async testing
        time.sleep(random.uniform(0.5, 1.5))
        
        print("\n" + "=" * 50)
        print("🔥 OTP GENERATED (DEV/ASYNC MODE)")
        print(f"📧 Email: {to_email}")
        print(f"🎯 Purpose: {purpose}")
        print(f"🔐 OTP: {otp}")
        print("=" * 50 + "\n")

        logger.info(f"[OTP EMAIL] {to_email} | {purpose} | OTP: {otp}")
