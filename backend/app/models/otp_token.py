from app.core.extensions import db
from datetime import datetime

class OTPToken(db.Model):
    """
    OTP Token model for email verification and password resets.
    OTPs are hashed before storage.
    """
    __tablename__ = "otp_tokens"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    # Hashed version of the 6-digit OTP
    otp_hash = db.Column(db.String(255), nullable=False)
    
    purpose = db.Column(db.String(50), nullable=False) # VERIFY_EMAIL | RESET_PASSWORD
    
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False, nullable=False)
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def is_expired(self):
        return datetime.utcnow() > self.expires_at

    def __repr__(self):
        return f"<OTPToken {self.purpose} for User {self.user_id}>"
