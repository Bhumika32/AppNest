"""
app/__init__.py

Application factory for AppNest.
Initializes Flask app, extensions, and registers routes.
"""

from flask import Flask
from flask_cors import CORS
from app.core.config import Config
from app.core.extensions import db, migrate, mail, jwt, socketio
from app.domain.notification_handlers import register_notification_handlers

# Blueprints
from app.api.routes.auth_routes import auth_bp
from app.api.routes.main_routes import main_bp
from app.api.routes.roast_routes import roast_bp
from app.api.routes.profile_routes import profile_bp
from app.api.routes.admin_routes import admin_bp
from app.api.routes.module_routes import module_bp, admin_module_bp
from app.api.routes.notification_routes import notification_bp
from app.domain.notification_handlers import register_notification_handlers

register_notification_handlers()
def create_app():
    """Create and configure the Flask application instance."""

    flask_app = Flask(__name__)
    flask_app.config.from_object(Config)
    
    # Explicit JWT Settings
    flask_app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    flask_app.config["JWT_HEADER_NAME"] = "Authorization"
    flask_app.config["JWT_HEADER_TYPE"] = "Bearer"
    flask_app.config["JWT_ERROR_MESSAGE_KEY"] = "error"

    # -------------------------
    # Initialize extensions
    # -------------------------
    db.init_app(flask_app)
    migrate.init_app(flask_app, db)
    mail.init_app(flask_app)
    jwt.init_app(flask_app)
    socketio.init_app(flask_app)

    # Register event handlers for notifications AFTER extension init
    register_notification_handlers()

    # Allow CORS for frontend with credentials (cookies)
    allowed_origins = flask_app.config.get("CORS_ORIGINS", [
        "http://localhost:5173", 
        "http://localhost:5174", 
        "http://localhost:5175",
        "http://localhost:5176",
    ])
    CORS(flask_app, supports_credentials=True, resources={
        r"/api/*": {
            "origins": allowed_origins
        }
    })

    # Create database tables if they don't exist
    with flask_app.app_context():
        db.create_all()
        
        # Initialize module discovery
        from app.platform.module_registry import ModuleRegistry
        ModuleRegistry._discover_modules()

        # Import WebSocket events to register handlers
        import app.api.routes.ws_events

    # -------------------------
    # Import models for migrations
    # -------------------------
    from app.models import User  # noqa: F401

    # -------------------------
    # Register core blueprints
    # -------------------------
    flask_app.register_blueprint(auth_bp)
    flask_app.register_blueprint(main_bp)
    flask_app.register_blueprint(roast_bp)
    flask_app.register_blueprint(profile_bp)
    flask_app.register_blueprint(admin_bp)
    flask_app.register_blueprint(module_bp)
    flask_app.register_blueprint(admin_module_bp)
    flask_app.register_blueprint(notification_bp)
    flask_app.url_map.strict_slashes = False

    return flask_app
