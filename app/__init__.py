"""
app/__init__.py

Application factory for AppNest.
Initializes Flask app, extensions, and registers routes.
"""

from flask import Flask
from app.config import Config
from app.extensions import db, migrate, mail
from app.routes.feedback_routes import feedback_bp 

# Import blueprints
from app.routes.auth_routes import auth_bp
from app.routes.main_routes import main_bp
from app.routes.tools_routes import tools_bp
from app.tools import register_tool_blueprints

def create_app():
    """Create and configure the Flask application instance."""

    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    # Import models so migrations can detect schema properly
    from app.models import User
    register_tool_blueprints(app)
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(tools_bp, url_prefix="/tools")
    app.register_blueprint(feedback_bp)
    return app