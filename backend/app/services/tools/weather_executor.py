from app.platform.module_executor import ModuleExecutor

"""
app/services/tools/weather.py

Weather service using OpenWeatherMap API.

Features:
- Real-time weather data
- Temperature in Celsius
- Weather condition details
- Error handling
"""

import requests
import os
from dataclasses import dataclass
from typing import Optional


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
    """Service class for weather data retrieval."""

    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    @staticmethod
    def get_weather(city: str) -> WeatherData:
        """
        Fetch weather data for a city.

        Args:
            city: City name

        Returns:
            WeatherData object with current conditions

        Raises:
            ValueError: If city not found or API error
        """
        api_key = os.getenv("OPENWEATHER_API_KEY")

        if not api_key:
            raise ValueError("OpenWeatherMap API key not configured")

        if not city or not city.strip():
            raise ValueError("City name is required")

        params = {
            "q": city.strip(),
            "appid": api_key,
            "units": "metric"  # Celsius
        }

        try:
            response = requests.get(
                WeatherService.BASE_URL,
                params=params,
                timeout=10
            )
            response.raise_for_status()

            data = response.json()

            # Check for API error response
            if response.status_code != 200:
                error_msg = data.get("message", "City not found")
                raise ValueError(error_msg)

            return WeatherData(
                city=data["name"],
                country=data["sys"]["country"],
                temperature=data["main"]["temp"],
                feels_like=data["main"]["feels_like"],
                humidity=data["main"]["humidity"],
                wind_speed=data["wind"]["speed"],
                condition=data["weather"][0]["main"],
                description=data["weather"][0]["description"].title(),
                pressure=data["main"]["pressure"],
                visibility=data.get("visibility", 0)
            )
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Weather API error: {str(e)}")
        except KeyError as e:
            raise ValueError(f"Missing weather data field: {str(e)}")



class WeatherExecutor(ModuleExecutor):
    module_key = "weather"

    def execute(self, payload: dict, user):
        metadata = payload.get("metadata", {})
        city = payload.get("city") or metadata.get("city")
        
        if not city:
            raise ValueError("city is required")
        return {
            "city": result.city,
            "country": result.country,
            "temperature": result.temperature,
            "feels_like": result.feels_like,
            "humidity": result.humidity,
            "wind_speed": result.wind_speed,
            "condition": result.condition,
            "description": result.description,
            "pressure": result.pressure,
            "visibility": result.visibility
        }
