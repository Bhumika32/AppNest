"""
app/tools/bmi/service.py

BMI tool business logic.
Keeps calculation separate from Flask routing for clean architecture.
"""


class BMIService:
    """Service class for BMI calculation."""

    @staticmethod
    def calculate_bmi(weight_kg: float, height_cm: float) -> tuple[float, str]:
        """
        Calculate BMI using weight (kg) and height (cm).

        Returns:
            (bmi_value, category)
        """
        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)

        category = BMIService.get_category(bmi)
        return round(bmi, 2), category

    @staticmethod
    def get_category(bmi: float) -> str:
        """Return BMI category based on standard BMI ranges."""
        if bmi < 18.5:
            return "Underweight"
        if 18.5 <= bmi < 25:
            return "Normal"
        if 25 <= bmi < 30:
            return "Overweight"
        return "Obese"