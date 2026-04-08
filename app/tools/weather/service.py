import requests
import os


class WeatherService:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    @staticmethod
    def get_weather(city: str) -> tuple[bool, str, dict | None]:
        api_key = os.getenv("OPENWEATHER_API_KEY")

        if not api_key:
            return False, "Missing OPENWEATHER_API_KEY in .env", None

        if not city.strip():
            return False, "City name is required.", None

        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"
        }

        try:
            res = requests.get(WeatherService.BASE_URL, params=params, timeout=10)
            data = res.json()

            if res.status_code != 200:
                return False, data.get("message", "City not found."), None

            weather_data = {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temp": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "wind": data["wind"]["speed"],
                "condition": data["weather"][0]["main"],
                "description": data["weather"][0]["description"].title(),
            }

            return True, "Weather fetched successfully.", weather_data

        except Exception as e:
            return False, f"Weather API error: {str(e)}", None