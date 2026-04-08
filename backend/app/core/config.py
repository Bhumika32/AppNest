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
