from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from app.extensions import db
from app.models.feedback import Feedback
from app.utils.auth_decorators import login_required

feedback_bp = Blueprint("feedback", __name__)

@feedback_bp.route("/feedback", methods=["GET", "POST"])
@login_required
def feedback():
    if request.method == "POST":
        message = request.form.get("message", "").strip()
        rating = request.form.get("rating", "").strip()

        if not message:
            flash("Message cannot be empty.", "danger")
            return redirect(url_for("feedback.feedback"))

        try:
            rating_int = int(rating)
            if rating_int < 1 or rating_int > 5:
                flash("Rating must be between 1 and 5.", "danger")
                return redirect(url_for("feedback.feedback"))
        except:
            flash("Rating must be a number.", "danger")
            return redirect(url_for("feedback.feedback"))

        fb = Feedback(
            user_id=session.get("user_id"),
            message=message,
            rating=rating_int,
        )

        db.session.add(fb)
        db.session.commit()

        flash("Thanks! Feedback submitted.", "success")
        return redirect(url_for("feedback.feedback"))

    return render_template("main/feedback.html")