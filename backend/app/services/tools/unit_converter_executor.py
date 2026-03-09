from app.platform.module_executor import ModuleExecutor

"""
app/services/tools/unit_converter.py

Unit conversion service supporting multiple unit types.

Features:
- Temperature conversion (C, F, K)
- Length conversion (m, km, miles, feet, inches)
- Weight conversion (kg, g, lb, oz)
- Volume conversion (L, ml, gallon)
- Professional error handling
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class UnitConversionResult:
    """Structured unit conversion result."""
    value: float
    from_unit: str
    to_unit: str
    converted_value: float
    category: str


class UnitConverterService:
    """Service class for unit conversions."""

    # Conversion factors to base units
    CONVERSIONS = {
        'temperature': {
            'celsius': {'name': '°C', 'base': 'celsius'},
            'fahrenheit': {'name': '°F', 'base': 'fahrenheit'},
            'kelvin': {'name': 'K', 'base': 'kelvin'},
        },
        'length': {
            'meter': {'name': 'm', 'to_base': 1},
            'kilometer': {'name': 'km', 'to_base': 1000},
            'centimeter': {'name': 'cm', 'to_base': 0.01},
            'millimeter': {'name': 'mm', 'to_base': 0.001},
            'mile': {'name': 'mi', 'to_base': 1609.34},
            'yard': {'name': 'yd', 'to_base': 0.9144},
            'foot': {'name': 'ft', 'to_base': 0.3048},
            'inch': {'name': 'in', 'to_base': 0.0254},
        },
        'weight': {
            'kilogram': {'name': 'kg', 'to_base': 1},
            'gram': {'name': 'g', 'to_base': 0.001},
            'milligram': {'name': 'mg', 'to_base': 0.000001},
            'pound': {'name': 'lb', 'to_base': 0.453592},
            'ounce': {'name': 'oz', 'to_base': 0.0283495},
        },
        'volume': {
            'liter': {'name': 'L', 'to_base': 1},
            'milliliter': {'name': 'ml', 'to_base': 0.001},
            'gallon': {'name': 'gal', 'to_base': 3.78541},
            'cup': {'name': 'cup', 'to_base': 0.236588},
            'tablespoon': {'name': 'tbsp', 'to_base': 0.0147868},
            'teaspoon': {'name': 'tsp', 'to_base': 0.00492892},
        },
    }

    @staticmethod
    def _celsius_to_fahrenheit(celsius: float) -> float:
        """Convert Celsius to Fahrenheit."""
        return (celsius * 9 / 5) + 32

    @staticmethod
    def _fahrenheit_to_celsius(fahrenheit: float) -> float:
        """Convert Fahrenheit to Celsius."""
        return (fahrenheit - 32) * 5 / 9

    @staticmethod
    def _celsius_to_kelvin(celsius: float) -> float:
        """Convert Celsius to Kelvin."""
        return celsius + 273.15

    @staticmethod
    def _kelvin_to_celsius(kelvin: float) -> float:
        """Convert Kelvin to Celsius."""
        return kelvin - 273.15

    @staticmethod
    def _fahrenheit_to_kelvin(fahrenheit: float) -> float:
        """Convert Fahrenheit to Kelvin."""
        celsius = UnitConverterService._fahrenheit_to_celsius(fahrenheit)
        return UnitConverterService._celsius_to_kelvin(celsius)

    @staticmethod
    def _kelvin_to_fahrenheit(kelvin: float) -> float:
        """Convert Kelvin to Fahrenheit."""
        celsius = UnitConverterService._kelvin_to_celsius(kelvin)
        return UnitConverterService._celsius_to_fahrenheit(celsius)

    @staticmethod
    def convert(
        value: float, from_unit: str, to_unit: str, category: str
    ) -> UnitConversionResult:
        """
        Convert between units in same category.

        Args:
            value: Value to convert
            from_unit: Source unit (e.g., 'meter', 'kilogram')
            to_unit: Target unit (e.g., 'kilometer', 'gram')
            category: Unit category (length, weight, temperature, volume)

        Returns:
            UnitConversionResult with converted value

        Raises:
            ValueError: If units or category invalid
        """
        category = category.lower()
        from_unit = from_unit.lower()
        to_unit = to_unit.lower()

        if category not in UnitConverterService.CONVERSIONS:
            raise ValueError(f"Unknown unit category: {category}")

        units = UnitConverterService.CONVERSIONS[category]

        if from_unit not in units:
            raise ValueError(f"Unknown unit: {from_unit} in category {category}")
        if to_unit not in units:
            raise ValueError(f"Unknown unit: {to_unit} in category {category}")

        if category == 'temperature':
            # Temperature conversions
            if from_unit == 'celsius' and to_unit == 'fahrenheit':
                converted = UnitConverterService._celsius_to_fahrenheit(value)
            elif from_unit == 'celsius' and to_unit == 'kelvin':
                converted = UnitConverterService._celsius_to_kelvin(value)
            elif from_unit == 'fahrenheit' and to_unit == 'celsius':
                converted = UnitConverterService._fahrenheit_to_celsius(value)
            elif from_unit == 'fahrenheit' and to_unit == 'kelvin':
                converted = UnitConverterService._fahrenheit_to_kelvin(value)
            elif from_unit == 'kelvin' and to_unit == 'celsius':
                converted = UnitConverterService._kelvin_to_celsius(value)
            elif from_unit == 'kelvin' and to_unit == 'fahrenheit':
                converted = UnitConverterService._kelvin_to_fahrenheit(value)
            else:
                converted = value
        else:
            # Other unit conversions
            base_value = value * units[from_unit]['to_base']
            converted = base_value / units[to_unit]['to_base']

        return UnitConversionResult(
            value=value,
            from_unit=from_unit,
            to_unit=to_unit,
            converted_value=round(converted, 4),
            category=category,
        )

    @staticmethod
    def get_units_for_category(category: str) -> List[Dict]:
        """Get all available units in a category."""
        category = category.lower()
        if category not in UnitConverterService.CONVERSIONS:
            return []
        
        units = UnitConverterService.CONVERSIONS[category]
        return [
            {"name": unit, "symbol": info["name"]}
            for unit, info in units.items()
        ]



class UnitConverterExecutor(ModuleExecutor):
    module_key = "unit-converter"

    def execute(self, payload: dict, user):
        metadata = payload.get("metadata", {})
        
        # Mapping for UnitConverter.jsx metadata fields
        value = payload.get("value") or metadata.get("amount") or metadata.get("value")
        from_unit = payload.get("from_unit") or metadata.get("from") or metadata.get("from_unit")
        to_unit = payload.get("to_unit") or metadata.get("to") or metadata.get("to_unit")
        category = payload.get("category") or metadata.get("category")

        if value is None or not from_unit or not to_unit or not category:
            return {"error": "INVALID_INPUT", "message": "value, from_unit, to_unit, and category are required"}

        UNIT_ALIASES = {
            "m": "meter", "km": "kilometer", "cm": "centimeter", "mm": "millimeter",
            "mi": "mile", "yd": "yard", "ft": "foot", "in": "inch",
            "kg": "kilogram", "g": "gram", "mg": "milligram", "lb": "pound", "oz": "ounce",
            "l": "liter", "ml": "milliliter", "gal": "gallon",
            "cup": "cup", "tbsp": "tablespoon", "tsp": "teaspoon",
            "c": "celsius", "f": "fahrenheit", "k": "kelvin"
        }

        from_unit = UNIT_ALIASES.get(from_unit.lower(), from_unit.lower())
        to_unit = UNIT_ALIASES.get(to_unit.lower(), to_unit.lower())

        try:
            result = UnitConverterService.convert(float(value), from_unit, to_unit, category)
        except ValueError as e:
            return {"error": "INVALID_INPUT", "message": str(e)}
            
        return {
            "value": result.value,
            "from_unit": result.from_unit,
            "to_unit": result.to_unit,
            "converted_value": result.converted_value,
            "category": result.category
        }
