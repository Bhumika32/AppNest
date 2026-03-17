# File: app/core/database.py

from typing import Generator
from sqlalchemy.orm import Session
from app.core.extensions import SessionLocal

def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a request-scoped DB session.
    Each request gets its own session.
    """
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()