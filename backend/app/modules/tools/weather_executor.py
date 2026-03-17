from app.platform.module_executor import ModuleExecutor
from app.platform.module_result import ModuleResult
from app.core.redis_client import neural_cache
import requests
import os
import time
from dataclasses import dataclass, asdict

"""
Weather service using OpenWeatherMap API with Neural Cache (Redis).
"""

CACHE_TTL = 1800  # 30 minutes cache for production

@dataclass
class WeatherData:
    """Structured weather data."""
    city: str
    country: str
    temperature: float
    feels_like: float
    humidity: int
    wind_speed: float
    condition: str
    description: str
    pressure: int
    visibility: int

class WeatherService:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    @staticmethod
    def get_weather(city: str) -> dict:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            raise ValueError("OpenWeatherMap API key not configured")

        city_key = f"weather:{city.strip().lower()}"
        
        # 1. Try Neural Cache (Redis)
        cached_data = neural_cache.get(city_key)
        if cached_data:
            return cached_data

        params = {
            "q": city.strip(),
            "appid": api_key,
            "units": "metric"
        }

        try:
            response = requests.get(WeatherService.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            result = {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
                "condition": data["weather"][0]["main"],
                "description": data["weather"][0]["description"].title(),
                "pressure": data["main"]["pressure"],
                "visibility": data.get("visibility", 0)
            }
            
            # 2. Store in Neural Cache
            neural_cache.set(city_key, result, ex=CACHE_TTL)
            return result
        except Exception as e:
            raise ValueError(f"Weather API error: {str(e)}")

import logging
logger = logging.getLogger(__name__)

class WeatherExecutor(ModuleExecutor):
    module_key = "weather"

    def execute(self, payload: dict, user) -> ModuleResult:
        logger.info(f"Executing Weather tool for user: {user.id}")
        metadata = payload.get("metadata", {})
        city = payload.get("city") or metadata.get("city")

        if not city:
            return ModuleResult(
                completed=False,
                status="error",
                error="INVALID_INPUT",
                message="city is required"
            )

        try:
            data = WeatherService.get_weather(city)
            return ModuleResult(
                completed=True,
                status="success",
                data=data
            )
        except ValueError as e:
            return ModuleResult(
                completed=False,
                status="error",
                error="SERVICE_ERROR",
                message=str(e)
            )