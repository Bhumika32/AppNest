from datetime import datetime, timedelta
from flask import current_app
from flask_jwt_extended import create_access_token, decode_token

class JWTManager:
    """
    Custom JWT management logic for short-lived access tokens.
    """
    
    @staticmethod
    def issue_access_token(user_id, role, session_id):
        """
        Create a short-lived access token containing role and session info.
        """
        additional_claims = {
            "role": (role or "user").lower(),  # Normalize to lowercase for consistency
            "session_id": session_id
        }
        
        # Access tokens should be very short-lived (10-15 mins)
        expires_delta = timedelta(minutes=15)
        
        return create_access_token(
            identity=str(user_id),
            additional_claims=additional_claims,
            expires_delta=expires_delta
        )

    @staticmethod
    def validate_token(token):
        """
        Decode and validate a token manually if needed.
        """
        try:
            return decode_token(token)
        except Exception:
            return None
