"""
app/services/otp_service.py

Real-world OTP implementation for AppNest.

Features:
- OTP generation (6 digits)
- Email sending via Flask-Mail
- 10 minute expiry (configurable)
- Attempt limiting
- Resend limiting with cooldown protection

Storage:
- OTP is stored in Flask session temporarily for simplicity.
- In production: use Redis or a dedicated OTP storage table.
"""

import random
from datetime import datetime, timedelta, timezone

from flask import session
from flask_mail import Message

from app.extensions import mail


class OTPService:
    """OTP generation + validation + email sender service."""

    OTP_LENGTH = 6
    OTP_EXPIRY_MINUTES = 10
    OTP_MAX_ATTEMPTS = 5
    OTP_MAX_RESENDS = 3
    OTP_RESEND_COOLDOWN_SECONDS = 30

    @staticmethod
    def _utc_now() -> datetime:
        """Return timezone-aware UTC datetime."""
        return datetime.now(timezone.utc)

    @staticmethod
    def generate_otp(length: int = OTP_LENGTH) -> str:
        """
        Generate a numeric OTP.

        Returns:
            str: OTP code
        """
        return "".join(str(random.randint(0, 9)) for _ in range(length))

    @classmethod
    def create_and_store_otp(cls, email: str, purpose: str) -> str:
        """
        Create OTP and store OTP-related metadata in session.

        Args:
            email: receiver email address
            purpose: verification/reset label

        Returns:
            str: generated otp
        """
        otp = cls.generate_otp()

        now = cls._utc_now()
        expires_at = now + timedelta(minutes=cls.OTP_EXPIRY_MINUTES)

        session["otp_email"] = email
        session["otp_purpose"] = purpose
        session["otp_code"] = otp
        session["otp_expires_at"] = expires_at.isoformat()
        session["otp_attempts"] = 0
        session["otp_resend_count"] = session.get("otp_resend_count", 0)
        session["otp_last_sent_at"] = now.isoformat()

        return otp

    @classmethod
    def can_resend(cls) -> tuple[bool, str]:
        """
        Check resend rules:
        - resend limit
        - cooldown time

        Returns:
            (allowed, message)
        """
        resend_count = session.get("otp_resend_count", 0)

        if resend_count >= cls.OTP_MAX_RESENDS:
            return False, "Resend limit exceeded. Please try again later."

        last_sent_str = session.get("otp_last_sent_at")
        if last_sent_str:
            last_sent = datetime.fromisoformat(last_sent_str)
            diff_seconds = (cls._utc_now() - last_sent).total_seconds()

            if diff_seconds < cls.OTP_RESEND_COOLDOWN_SECONDS:
                wait = int(cls.OTP_RESEND_COOLDOWN_SECONDS - diff_seconds)
                return False, f"Please wait {wait}s before resending OTP."

        return True, "Resend allowed."

    @classmethod
    def resend_otp(cls) -> tuple[bool, str]:
        """
        Generate a new OTP, enforce resend rules, and send it again.
        """
        allowed, msg = cls.can_resend()
        if not allowed:
            return False, msg

        email = session.get("otp_email")
        purpose = session.get("otp_purpose")

        if not email or not purpose:
            return False, "OTP session expired. Please register again."

        session["otp_resend_count"] = session.get("otp_resend_count", 0) + 1

        otp = cls.create_and_store_otp(email=email, purpose=purpose)
        cls.send_otp_email(to_email=email, otp=otp, purpose=purpose)

        return True, "OTP resent successfully."

    @classmethod
    def verify_otp(cls, submitted_otp: str) -> tuple[bool, str]:
        """
        Verify OTP with expiry and attempt limit.

        Returns:
            (success, message)
        """
        stored_otp = session.get("otp_code")
        expires_at_str = session.get("otp_expires_at")

        if not stored_otp or not expires_at_str:
            return False, "OTP session not found. Please request OTP again."

        expires_at = datetime.fromisoformat(expires_at_str)

        # Check expiry
        if cls._utc_now() > expires_at:
            return False, "OTP expired. Please resend OTP."

        # Check attempts
        attempts = session.get("otp_attempts", 0)
        if attempts >= cls.OTP_MAX_ATTEMPTS:
            return False, "Too many wrong attempts. Please resend OTP."

        # Increment attempts and validate
        session["otp_attempts"] = attempts + 1

        if submitted_otp != stored_otp:
            remaining = cls.OTP_MAX_ATTEMPTS - session["otp_attempts"]
            return False, f"Invalid OTP. Attempts left: {remaining}"

        return True, "OTP verified successfully."

    @staticmethod
    def send_otp_email(to_email: str, otp: str, purpose: str = "Verification") -> None:
        """
        Send OTP email using Flask-Mail.

        Args:
            to_email: receiver email
            otp: OTP code
            purpose: message category
        """
        msg = Message(
            subject=f"AppNest OTP - {purpose}",
            recipients=[to_email],
            body=f"""Your AppNest OTP is: {otp}

This OTP expires in 10 minutes.

If you did not request this OTP, ignore this email.
"""
        )
        mail.send(msg)

    @staticmethod
    def clear_otp_session() -> None:
        """
        Clear OTP-related session keys after successful verification
        or when restarting the flow.
        """
        for key in [
            "otp_email",
            "otp_purpose",
            "otp_code",
            "otp_expires_at",
            "otp_attempts",
            "otp_resend_count",
            "otp_last_sent_at",
        ]:
            session.pop(key, None)