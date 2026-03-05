import random
from datetime import datetime, timedelta, timezone

from flask_mail import Message
from app.core.extensions import db, mail
from app.models.otp_token import OTPToken
from app.models.user import User
from app.core.security import hash_data, verify_hash

class OTPService:
    """OTP generation + validation + email sender service using database storage."""

    OTP_LENGTH = 6
    OTP_EXPIRY_MINUTES = 10
    OTP_RESEND_COOLDOWN_SECONDS = 60
    MAX_DAILY_OTPS = 5
    MAX_FAILED_ATTEMPTS = 3

    @staticmethod
    def _utc_now() -> datetime:
        """Return naive UTC datetime (SQLAlchemy standard)."""
        return datetime.utcnow()

    @staticmethod
    def generate_otp(length: int = OTP_LENGTH) -> str:
        return "".join(str(random.randint(0, 9)) for _ in range(length))

    @classmethod
    def create_and_store_otp(cls, email: str, purpose: str) -> str:
        """
        Create OTP, hash it, and store in the database.
        Invalidates any previous unused OTPs for this user/purpose.
        """
        user = User.query.filter_by(email=email).first()
        if not user:
            raise ValueError("User not found for OTP generation")
            
        # Abuse Protection: Check daily limit
        today_start = cls._utc_now().replace(hour=0, minute=0, second=0, microsecond=0)
        daily_count = OTPToken.query.filter(
            OTPToken.user_id == user.id,
            OTPToken.purpose == purpose,
            OTPToken.created_at >= today_start
        ).count()
        
        if daily_count >= cls.MAX_DAILY_OTPS:
            # We don't raise error to avoid leaking user info easily, but silently refuse
            # Or raise if we want the controller to handle it
            raise ValueError(f"Daily limit of {cls.MAX_DAILY_OTPS} OTPs reached. Try again tomorrow.")

        # Invalidate previous unused OTPs for this purpose
        for old_otp in OTPToken.query.filter_by(user_id=user.id, purpose=purpose, used=False).all():
            old_otp.used = True

        otp = cls.generate_otp()
        hashed_otp = hash_data(otp)
        
        expires_at = cls._utc_now() + timedelta(minutes=cls.OTP_EXPIRY_MINUTES)

        otp_token = OTPToken(
            user_id=user.id,
            otp_hash=hashed_otp,
            purpose=purpose,
            expires_at=expires_at
        )
        
        db.session.add(otp_token)
        db.session.commit()

        return otp

    @classmethod
    def can_resend(cls, email: str) -> tuple[bool, str]:
        """
        Check resend rules: 1 minute cooldown per email.
        """
        user = User.query.filter_by(email=email).first()
        if not user:
            return False, "User not found."

        latest_otp = OTPToken.query.filter_by(user_id=user.id).order_by(OTPToken.created_at.desc()).first()
        
        if latest_otp:
            # SQLAlchemy created_at might be naive, ensure comparison is consistent
            diff_seconds = (cls._utc_now() - latest_otp.created_at).total_seconds()
            if diff_seconds < cls.OTP_RESEND_COOLDOWN_SECONDS:
                wait = int(cls.OTP_RESEND_COOLDOWN_SECONDS - diff_seconds)
                return False, f"Please wait {wait}s before resending OTP."

        return True, "Resend allowed."

    @classmethod
    def verify_otp(cls, email: str, submitted_otp: str) -> tuple[bool, str]:
        """
        Verify hashed OTP from database.
        """
        user = User.query.filter_by(email=email).first()
        if not user:
            return False, "User not found."

        # Find the latest unused and non-expired OTP for this user
        otp_token = OTPToken.query.filter_by(
            user_id=user.id, 
            used=False
        ).order_by(OTPToken.created_at.desc()).first()

        if not otp_token:
            return False, "No active OTP found. Please request a new one."

        if otp_token.is_expired():
            otp_token.used = True
            db.session.commit()
            return False, "OTP has expired. Please request a new one."
            
        # Implementing basic abuse protection for failed attempts
        if getattr(otp_token, 'failed_attempts', 0) >= cls.MAX_FAILED_ATTEMPTS:
             otp_token.used = True
             db.session.commit()
             return False, "Too many failed attempts. OTP invalidated. Request a new one."

        if not verify_hash(submitted_otp, otp_token.otp_hash):
            if hasattr(otp_token, 'failed_attempts'):
                otp_token.failed_attempts += 1
                db.session.commit()
            return False, "Invalid OTP."

        # Mark as used
        otp_token.used = True
        db.session.commit()

        return True, "OTP verified successfully."

    @staticmethod
    def send_otp_email(to_email: str, otp: str, purpose: str = "Verification") -> None:
        msg = Message(
            subject=f"AppNest OTP - {purpose}",
            recipients=[to_email],
            body=f"Your AppNest OTP is: {otp}\n\nThis OTP expires in 10 minutes.\n\nIf you did not request this OTP, ignore this email."
        )
        try:
            mail.send(msg)
            print(f"✅ [EMAIL SENT] OTP for {to_email}: {otp}")
        except Exception as e:
            print(f"⚠️ [EMAIL FAILED] {e} | 🔑 [DEV MODE] OTP for {to_email}: {otp}")