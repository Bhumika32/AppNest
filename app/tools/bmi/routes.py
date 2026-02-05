"""
app/tools/bmi/routes.py

BMI tool routes.
Handles:
- Form input
- Validation
- Showing output
"""

from flask import Blueprint, render_template, request, flash
from app.utils.auth_decorators import login_required
from app.tools.bmi.service import BMIService

bmi_bp = Blueprint("bmi", __name__)


@bmi_bp.route("/", methods=["GET", "POST"])
@login_required
def bmi_home():
    """
    BMI Calculator page.

    GET:
        Show BMI form
    POST:
        Calculate BMI and show result
    """
    bmi_result = None
    bmi_category = None

    if request.method == "POST":
        try:
            weight = float(request.form.get("weight", 0))
            height = float(request.form.get("height", 0))

            if weight <= 0 or height <= 0:
                flash("Height and Weight must be positive values.", "error")
                return render_template("tools/bmi.html")

            bmi_result, bmi_category = BMIService.calculate_bmi(weight, height)

        except ValueError:
            flash("Please enter valid numeric values.", "error")

    return render_template(
        "tools/bmi.html",
        bmi=bmi_result,
        category=bmi_category
    )