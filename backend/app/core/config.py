"""
app/config.py

Central configuration for AppNest.
Loads environment variables from .env so secrets are never hardcoded in code.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Flask configuration loaded from environment variables."""

    # Flask secret key (required for session security)
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-this-secret")
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    JWT_REFRESH_TOKEN_EXPIRES = 86400  # 1 day


    # Database connection string (SQLAlchemy)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "mysql+pymysql://root:root@localhost/app_nest"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mail configuration (used for OTP and password reset)
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    # Optional: define sender name shown in email
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", os.getenv("MAIL_USERNAME"))