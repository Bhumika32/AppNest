"""
app/services/tools_registry.py

Central registry for all tools available in AppNest.
Dashboard and tools index will be generated dynamically from this list.
"""

from dataclasses import dataclass


@dataclass
class ToolItem:
    """Represents one tool in AppNest."""
    name: str
    description: str
    url: str
    icon: str = "🧩"


class ToolsRegistry:
    """Returns the list of available tools (dynamic dashboard rendering)."""

    @staticmethod
    def get_tools() -> list[ToolItem]:
        return [
            ToolItem(
                name="BMI Calculator",
                description="Calculate BMI using height and weight.",
                url="/tools/bmi/",
                icon="⚖️",
            ),
            ToolItem(
                name="Currency Converter",
                description="Convert currencies using live exchange rates.",
                url="/tools/currency/",
                icon="💱",
            ),
            ToolItem(
                name="Weather Checker",
                description="Get live weather info by city name.",
                url="/tools/weather/",
                icon="🌤️",
            ),
            ToolItem(
                name="Age Calculator",
                description="Calculate age + fun messages + birthday countdown.",
                url="/tools/age/",
                icon="🎂",
            ),
            ToolItem(
                name="Rashi Tool",
                description="Birthplace + time → Rashi with real facts + roast (Free OSM autocomplete).",
                url="/tools/rashi/",
                icon="🔮",
            ),
            ToolItem(
                name="MoodFix",
                description="Pick a mood → get roasted + motivated + a 5-min task 😈⚡",
                url="/tools/moodfix/",
                icon="😈",
            ),
            # Add more tools here step-by-step
        ]