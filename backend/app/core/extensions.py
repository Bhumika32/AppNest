"""
app/extensions.py

This module defines Flask extension singletons.
Extensions are created here and initialized inside create_app().

Why?
- Prevent circular imports
- Keep app factory clean
- Make the project scalable and testable
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

# Database ORM
db = SQLAlchemy()

# Migration engine
migrate = Migrate()

# Email (SMTP) integration for OTP / password reset
mail = Mail()
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO

jwt = JWTManager()

# WebSocket (Real-time notifications)
# cors_allowed_origins="*" for development, should be restricted in production
socketio = SocketIO(cors_allowed_origins="*")
