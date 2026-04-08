#!/usr/bin/env python
"""
Database initialization script.
Creates all tables in the database without using migrations.
"""

import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.core.database import Base as db

def init_db():
    """Initialize database with all tables."""
    app = create_app()
    
    with app.app_context():
        print("[INFO] Creating all database tables...")
        try:
            db.create_all()
            print("[OK] All tables created successfully!")
            return 0
        except Exception as e:
            print(f"[ERROR] Failed to create tables: {str(e)}")
            return 1

if __name__ == '__main__':
    sys.exit(init_db())
