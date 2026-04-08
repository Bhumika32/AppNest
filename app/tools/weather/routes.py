from flask import Blueprint, render_template, request, flash
from app.tools.weather.service import WeatherService

weather_bp = Blueprint("weather", __name__, url_prefix="/tools/weather")


@weather_bp.route("/", methods=["GET", "POST"])
def weather_home():
    weather = None

    if request.method == "POST":
        city = request.form.get("city", "")
        ok, msg, weather = WeatherService.get_weather(city)

        if not ok:
            flash(msg, "danger")

    return render_template("tools/weather.html", weather=weather)