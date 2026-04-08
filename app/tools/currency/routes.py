"""
app/tools/currency/routes.py

Currency Converter routes.
Provides UI and conversion output.
"""

from flask import Blueprint, render_template, request, flash
from app.utils.auth_decorators import login_required
from app.tools.currency.service import CurrencyService

currency_bp = Blueprint("currency", __name__)


@currency_bp.route("/", methods=["GET", "POST"])
@login_required
def currency_home():
    """
    Currency converter page.
    """
    result = None

    # Default currency values
    from_currency = "USD"
    to_currency = "INR"
    amount = 1.0

    try:
        symbols = CurrencyService.get_supported_symbols()
    except Exception:
        symbols = {
            "USD": "United States Dollar",
            "INR": "Indian Rupee",
            "EUR": "Euro",
            "GBP": "British Pound",
            "JPY": "Japanese Yen",
        }
        flash("Live currency list unavailable. Showing fallback list.", "error")

    if request.method == "POST":
        try:
            from_currency = request.form.get("from_currency", "USD")
            to_currency = request.form.get("to_currency", "INR")
            amount = float(request.form.get("amount", "1"))

            if amount <= 0:
                flash("Amount must be greater than 0.", "error")
                return render_template("tools/currency.html", symbols=symbols)

            result = CurrencyService.convert(amount, from_currency, to_currency)

        except ValueError:
            flash("Enter a valid numeric amount.", "error")
        except Exception as e:
            flash(f"Conversion failed: {str(e)}", "error")

    return render_template(
        "tools/currency.html",
        symbols=symbols,
        amount=amount,
        from_currency=from_currency,
        to_currency=to_currency,
        result=result,
        currency_service=CurrencyService,
    )