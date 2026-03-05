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
    allowed_origins = app.config.get("CORS_ORIGINS", [
        "http://localhost:5173", 
        "http://localhost:5174", 
        "http://localhost:5175",
        "http://localhost:5176",
    ])
    CORS(app, supports_credentials=True, resources={
        r"/api/*": {
            "origins": allowed_origins
        }
    })

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
        # Modules are seed-based or dynamic, no need for manifest scanning now
        
        # Auto-register module executors
        from app.platform.module_registry import register_executor
        from app.services.tools.bmi_executor import BMIExecutor
        from app.services.tools.currency_executor import CurrencyExecutor
        from app.services.tools.age_executor import AgeExecutor
        from app.services.tools.rashi_executor import RashiExecutor
        from app.services.tools.weather_executor import WeatherExecutor
        from app.services.tools.unit_converter_executor import UnitConverterExecutor
        
        from app.services.games.tictactoe_executor import TicTacToeExecutor
        from app.services.games.snake_executor import SnakeExecutor
        from app.services.games.flappy_bird_executor import FlappyBirdExecutor
        from app.services.games.brick_breaker_executor import BrickBreakerExecutor
        
        from app.services.tools.extra_executors import CGPAExecutor, JokeExecutor, TranslatorExecutor
        
        register_executor(BMIExecutor.module_key, BMIExecutor)
        register_executor(CurrencyExecutor.module_key, CurrencyExecutor)
        register_executor(AgeExecutor.module_key, AgeExecutor)
        register_executor(RashiExecutor.module_key, RashiExecutor)
        register_executor(WeatherExecutor.module_key, WeatherExecutor)
        register_executor(UnitConverterExecutor.module_key, UnitConverterExecutor)
        register_executor(CGPAExecutor.module_key, CGPAExecutor)
        register_executor(JokeExecutor.module_key, JokeExecutor)
        register_executor(TranslatorExecutor.module_key, TranslatorExecutor)
        
        register_executor(TicTacToeExecutor.module_key, TicTacToeExecutor)
        register_executor(SnakeExecutor.module_key, SnakeExecutor)
        register_executor(FlappyBirdExecutor.module_key, FlappyBirdExecutor)
        register_executor(BrickBreakerExecutor.module_key, BrickBreakerExecutor)


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
