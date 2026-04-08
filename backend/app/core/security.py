import hashlib
import hmac
import os
from werkzeug.security import generate_password_hash, check_password_hash

def hash_data(data: str) -> str:
    """
    General purpose hash (SHA-256) for OTPs and tokens before storage.
    """
    return hashlib.sha256(data.encode()).hexdigest()

def verify_hash(data: str, hashed_data: str) -> bool:
    """
    Verify data against its hash.
    """
    return hash_data(data) == hashed_data

def generate_secure_token() -> str:
    """
    Generate a cryptographically secure random token (e.g., for refresh tokens).
    """
    return os.urandom(32).hex()
