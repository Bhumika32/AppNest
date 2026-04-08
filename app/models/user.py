"""
app/models/user.py

This module defines the User database model.

Key responsibilities:
- Store user identity data (username, email)
- Store password securely as a hash (never plain text)
- Provide helper methods for setting/checking passwords
"""

from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    """
    User model used for authentication and identity management.

    Notes:
    - __tablename__ ensures consistent table naming in the database.
    - created_at is useful for auditing / sorting by registration time.
    """

    __tablename__ = "users"

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # Unique identity fields
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # Account verification flag (email OTP verification)
    is_verified = db.Column(db.Boolean, default=False, nullable=False)
    # Password hash storage (DO NOT store plain passwords)
    password_hash = db.Column(db.String(255), nullable=False)

    # Timestamp for user creation
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def set_password(self, password: str) -> None:
        """
        Hash and store the password.

        This method ensures passwords are always stored securely.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Verify a password against the stored password hash.

        Returns:
            bool: True if password is correct, otherwise False
        """
        return check_password_hash(self.password_hash, password)