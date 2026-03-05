from app.platform.module_executor import ModuleExecutor

"""
app/services/tools/bmi.py

BMI Calculator service with health category classification.

Features:
- Accurate BMI calculation
- Health category classification
- Health recommendations
- Professional output structure
"""

from dataclasses import dataclass


@dataclass
class BMIResult:
    """Structured BMI calculation result."""
    bmi: float
    category: str
    weight_kg: float
    height_cm: float
    recommendation: str


class BMIService:
    """Service class for BMI calculation."""

    BMI_CATEGORIES = {
        'underweight': {
            'min': 0,
            'max': 18.5,
            'label': 'Underweight',
            'color': 'blue',
            'recommendation': 'Consult a nutritionist to gain healthy weight.'
        },
        'normal': {
            'min': 18.5,
            'max': 25,
            'label': 'Normal Weight',
            'color': 'green',
            'recommendation': 'Maintain your current lifestyle with balanced diet and exercise.'
        },
        'overweight': {
            'min': 25,
            'max': 30,
            'label': 'Overweight',
            'color': 'yellow',
            'recommendation': 'Consider increasing physical activity and balanced nutrition.'
        },
        'obese': {
            'min': 30,
            'max': float('inf'),
            'label': 'Obese',
            'color': 'red',
            'recommendation': 'Consult a healthcare professional for personalized guidance.'
        },
    }

    @staticmethod
    def calculate_bmi(weight_kg: float, height_cm: float) -> BMIResult:
        """
        Calculate BMI using weight (kg) and height (cm).

        Args:
            weight_kg: Weight in kilograms
            height_cm: Height in centimeters

        Returns:
            BMIResult with calculated values and recommendations
        """
        # Validate inputs
        if weight_kg <= 0 or height_cm <= 0:
            raise ValueError("Weight and height must be positive numbers")

        # Calculate BMI
        height_m = height_cm / 100
        bmi_value = weight_kg / (height_m ** 2)

        # Get category and recommendation
        category_info = BMIService._get_category_info(bmi_value)

        return BMIResult(
            bmi=round(bmi_value, 2),
            category=category_info['label'],
            weight_kg=weight_kg,
            height_cm=height_cm,
            recommendation=category_info['recommendation']
        )

    @staticmethod
    def _get_category_info(bmi: float) -> dict:
        """Get category information for BMI value."""
        for category_key, category_data in BMIService.BMI_CATEGORIES.items():
            if category_data['min'] <= bmi < category_data['max']:
                return category_data
        return BMIService.BMI_CATEGORIES['obese']

    @staticmethod
    def get_all_categories() -> list:
        """Get all BMI categories for reference."""
        return [
            {
                'label': info['label'],
                'range': f"{info['min']:.1f} - {info['max'] if info['max'] != float('inf') else '∞'}",
                'color': info['color']
            }
            for info in BMIService.BMI_CATEGORIES.values()
        ]



class BMIExecutor(ModuleExecutor):
    module_key = "bmi-calculator"

    def execute(self, payload: dict, user):
        meta = payload.get("metadata", {})
        
        # Determine height/weight from top-level or metadata
        height = payload.get("height_cm") or payload.get("height") or meta.get("height_cm") or meta.get("height")
        weight = payload.get("weight_kg") or payload.get("weight") or meta.get("weight_kg") or meta.get("weight")

        if not height or not weight:
            raise ValueError("Height and weight are required")

        result = BMIService.calculate_bmi(float(weight), float(height))
        
        return {
            "bmi": result.bmi,
            "category": result.category,
            "weight_kg": result.weight_kg,
            "height_cm": result.height_cm,
            "recommendation": result.recommendation
        }
