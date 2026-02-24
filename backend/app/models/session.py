from app.core.extensions import db
import uuid
from datetime import datetime

class Session(db.Model):
    """
    Session model to track login instances and refresh tokens.
    Supports multi-device sessions and revocation.
    """
    __tablename__ = "sessions"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    
    # Hashed version of the refresh token
    refresh_token_hash = db.Column(db.String(255), unique=True, nullable=False)
    
    device_info = db.Column(db.String(255))
    ip_address = db.Column(db.String(45))
    
    expires_at = db.Column(db.DateTime, nullable=False)
    revoked = db.Column(db.Boolean, default=False, nullable=False)
    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    last_used_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    def is_expired(self):
        return datetime.utcnow() > self.expires_at

    def __repr__(self):
        return f"<Session {self.id} for User {self.user_id}>"
