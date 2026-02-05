"""
app/tools/rashi/routes.py

Rashi Tool page routes

✅ Inputs:
- Name
- Birth place (via autocomplete)
- Birth date
- Birth time
- Hidden lat/lon

✅ Uses RashiService
"""

from flask import Blueprint, render_template, request, flash
from app.utils.auth_decorators import login_required
from app.tools.rashi.service import RashiService

rashi_bp = Blueprint("rashi", __name__, url_prefix="/tools/rashi")


@rashi_bp.route("/", methods=["GET", "POST"])
@login_required
def rashi_home():
    result = None

    entered_name = ""
    birth_place = ""
    birth_time = ""
    birth_date = ""
    birth_lat = ""
    birth_lon = ""

    if request.method == "POST":
        entered_name = request.form.get("name", "").strip()
        birth_place = request.form.get("birth_place", "").strip()
        birth_time = request.form.get("birth_time", "").strip()
        birth_date = request.form.get("birth_date", "").strip()
        birth_lat = request.form.get("birth_lat", "").strip()
        birth_lon = request.form.get("birth_lon", "").strip()

        if not entered_name:
            flash("Name is required.", "danger")
        elif not birth_place:
            flash("Birth place is required.", "danger")
        elif not birth_date:
            flash("Birth date is required.", "danger")
        elif not birth_time:
            flash("Birth time is required.", "danger")
        elif not birth_lat or not birth_lon:
            flash("Select a location from dropdown (don’t type random 😭).", "warning")
        else:
            try:
                result = RashiService.calculate(
                    name=entered_name,
                    birth_place=birth_place,
                    birth_time=birth_time,
                    birth_date=birth_date,
                    birth_lat=birth_lat,
                    birth_lon=birth_lon,
                )

                flash(f"{result.headline} ✅", "success")

            except Exception as e:
                flash(f"Something went wrong: {str(e)}", "danger")
                result = None

    return render_template(
        "tools/rashi.html",
        result=result,
        entered_name=entered_name,
        birth_place=birth_place,
        birth_time=birth_time,
        birth_date=birth_date,
        birth_lat=birth_lat,
        birth_lon=birth_lon,
    )