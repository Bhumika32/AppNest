"""
app/__init__.py

Application factory for AppNest.
Initializes Flask app, extensions, and registers routes.
"""

from flask import Flask
from app.core.config import Config
from app.core.extensions import db, migrate, mail

# Blueprints
from app.api.auth_routes import auth_bp
from app.api.main_routes import main_bp
from app.api.feedback_routes import feedback_bp
from app.api.roast_routes import roast_bp
from app.api.profile_routes import profile_bp
from app.api.admin import admin_bp
from app.api.module_routes import module_bp, admin_module_bp
from app.api.notification_routes import notification_bp
from flask_cors import CORS
from app.core.extensions import db, migrate, mail, jwt

# Realm utilities
from app.utils.realm import get_active_realm


def create_app():
    """Create and configure the Flask application instance."""

    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Explicit JWT Settings
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    app.config["JWT_HEADER_NAME"] = "Authorization"
    app.config["JWT_HEADER_TYPE"] = "Bearer"
    app.config["JWT_ERROR_MESSAGE_KEY"] = "error"

    # -------------------------
    # Initialize extensions
    # -------------------------
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    jwt.init_app(app)
    # Allow CORS for frontend with credentials (cookies)
    # Support multiple common Vite ports in case 5173 is busy
    CORS(app, supports_credentials=True, resources={
        r"/api/*": {
            "origins": [
                "http://localhost:5173", 
                "http://localhost:5174", 
                "http://localhost:5175",
                "http://localhost:5176",
            ]
        }
    })

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
        # Modules are seed-based or dynamic, no need for manifest scanning now
        pass


    # -------------------------
    # Import models for migrations
    # -------------------------
    from app.models import User  # noqa: F401

    # -------------------------
    # Register core blueprints
    # -------------------------
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(feedback_bp)
    app.register_blueprint(roast_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(module_bp)
    app.register_blueprint(admin_module_bp)
    app.register_blueprint(notification_bp)
    app.url_map.strict_slashes = False


    # -------------------------
    # Inject active realm globally
    # -------------------------
    return app
