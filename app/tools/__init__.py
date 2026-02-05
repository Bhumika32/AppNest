"""
app/tools/__init__.py

Registers all tool modules under /tools/*
"""

from app.tools.bmi.routes import bmi_bp
from app.tools.currency.routes import currency_bp
from app.tools.weather.routes import weather_bp
from app.tools.age.routes import age_bp

from app.tools.rashi.api_routes import rashi_api_bp
from app.tools.rashi.routes import rashi_bp

from app.tools.moodfix.routes import moodfix_bp


def register_tool_blueprints(app):
    """Register tool blueprints."""
    app.register_blueprint(bmi_bp, url_prefix="/tools/bmi")
    app.register_blueprint(currency_bp, url_prefix="/tools/currency")
    app.register_blueprint(weather_bp, url_prefix="/tools/weather")
    app.register_blueprint(age_bp, url_prefix="/tools/age")

    app.register_blueprint(rashi_api_bp)
    app.register_blueprint(rashi_bp)

    app.register_blueprint(moodfix_bp)

    # ✅ Optional debug prints
    print("✅ Registered: bmi_bp (app.tools.bmi.routes)")
    print("✅ Registered: currency_bp (app.tools.currency.routes)")
    print("✅ Registered: weather_bp (app.tools.weather.routes)")
    print("✅ Registered: age_bp (app.tools.age.routes)")
    print("✅ Registered: rashi_api_bp (app.tools.rashi.api_routes)")
    print("✅ Registered: rashi_bp (app.tools.rashi.routes)")
    print("✅ Registered: moodfix_bp (app.tools.moodfix.routes)")