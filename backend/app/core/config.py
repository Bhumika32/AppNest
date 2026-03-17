"""app/core/config.py"""
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """
    Central configuration using Pydantic (FastAPI-native).
    Automatically validates env variables.
    """
    #  ENV
    ENV: str = "development"
    DEBUG: bool = True

    # Security
    SECRET_KEY: str
    JWT_SECRET_KEY: str

    JWT_ACCESS_TOKEN_EXPIRES: int = 3600
    JWT_REFRESH_TOKEN_EXPIRES: int = 86400

    # Database
    DATABASE_URL: str = "mysql+pymysql://root:root@localhost/app_nest"

    # Mail
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_PORT: int = 587
    MAIL_USE_TLS: bool = True
    MAIL_USERNAME: str | None = None
    MAIL_PASSWORD: str | None = None
    MAIL_DEFAULT_SENDER: str | None = None

    #  Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_SOCKET_TIMEOUT: int = 2
    REDIS_CONNECT_TIMEOUT: int = 2

    # 🤖 AI
    GEMINI_API_KEY: str | None = None

    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ]

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"


settings = Settings()
# """
# app/config.py

# Central configuration for AppNest.
# Loads environment variables from .env so secrets are never hardcoded in code.
# """

# import os
# from dotenv import load_dotenv

# load_dotenv()


# class Config:
#     """Base configuration"""

  
#     SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
#     JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-this-secret")
#     JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
#     JWT_REFRESH_TOKEN_EXPIRES = 86400  # 1 day

#     # Database connection string (SQLAlchemy)
#     SQLALCHEMY_DATABASE_URI = os.getenv(
#         "DATABASE_URL",
#         "mysql+pymysql://root:root@localhost/app_nest"
#     )
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

#     # Mail configuration (used for OTP and password reset)
#     MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
#     MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
#     MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "true").lower() == "true"
#     MAIL_USERNAME = os.getenv("MAIL_USERNAME")
#     MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
#     MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", os.getenv("MAIL_USERNAME"))

#     # Production Performance & AI Config
#     REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
#     GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

#     # CORS Configuration
#     CORS_ORIGINS = [
#         "http://localhost:5173",
#         "http://127.0.0.1:5173",
#         "http://localhost:5000",
#         "http://127.0.0.1:5000"
#     ]
