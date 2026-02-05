"""
app/tools/age/routes.py

Routes for Age Calculator tool.

URL:
- /tools/age/

Features:
- Name + DOB dropdown input (day/month/year)
- Fun Mode toggle (default ON)
- Roast Mode toggle (optional)
- Preserves selected dropdowns after submit
- Flash popup message with correct theme
"""

from datetime import date

from flask import Blueprint, render_template, request, flash

from app.utils.auth_decorators import login_required
from app.tools.age.service import AgeService


age_bp = Blueprint("age", __name__, url_prefix="/tools/age")


@age_bp.route("/", methods=["GET", "POST"])
@login_required
def age_home():
    result = None

    # ✅ Defaults for GET
    fun_mode = True
    roast_mode = False

    # ✅ Must exist even on GET (otherwise UnboundLocalError)
    entered_name = ""
    selected_day = ""
    selected_month = ""
    selected_year = ""

    if request.method == "POST":
        entered_name = request.form.get("name", "").strip()

        selected_day = request.form.get("dob_day", "").strip()
        selected_month = request.form.get("dob_month", "").strip()
        selected_year = request.form.get("dob_year", "").strip()

        fun_mode = request.form.get("fun_mode") == "on"
        roast_mode = request.form.get("roast_mode") == "on"

        # ✅ UX enforcement
        if roast_mode:
            fun_mode = True
        if not fun_mode:
            roast_mode = False

        # ✅ Validation
        if not entered_name:
            flash("Name is required.", "danger")
        elif not selected_day or not selected_month or not selected_year:
            flash("Please select complete Date of Birth (Day / Month / Year).", "danger")
        else:
            # ✅ Convert DOB dropdown -> date object
            try:
                dob = date(int(selected_year), int(selected_month), int(selected_day))

                # ✅ Calculate result
                result = AgeService.calculate(
                    name=entered_name,
                    dob=dob,
                    fun_mode=fun_mode,
                    roast_mode=roast_mode,
                )

                # ✅ Flash theme based on mode
                if roast_mode:
                    flash(result.message, "warning")   # yellow vibe
                elif fun_mode:
                    flash(result.message, "success")   # green vibe
                else:
                    flash("Age calculated successfully ✅", "success")

            except ValueError:
                flash("Invalid date selected. Please choose a valid DOB.", "danger")
            except Exception as e:
                flash(str(e), "danger")

    return render_template(
        "tools/age.html",
        result=result,
        fun_mode=fun_mode,
        roast_mode=roast_mode,
        entered_name=entered_name,
        selected_day=selected_day,
        selected_month=selected_month,
        selected_year=selected_year,
    )