"""
app/routes/feedback_routes.py

Feedback API endpoints.

IMPORTANT:
- JWT protected
- No sessions
- No template rendering
"""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.core.extensions import db
from app.models.feedback import Feedback

# Feedback-related API routes
feedback_bp = Blueprint("feedback", __name__, url_prefix="/api/feedback")


@feedback_bp.route("/", methods=["POST"])
@jwt_required()
def submit_feedback():
    """
    Submit feedback from an authenticated user.

    Expected input (JSON):
    {
        "message": "Great app",
        "rating": 5
    }
    """
    data = request.get_json() or {}

    message = data.get("message", "").strip()
    rating = data.get("rating")

    # Basic validation
    if not message or rating is None:
        return {"error": "Message and rating are required"}, 400

    user_id = get_jwt_identity()

    # Create feedback record
    feedback = Feedback(
        user_id=user_id,
        message=message,
        rating=int(rating)
    )

    db.session.add(feedback)
    db.session.commit()

    return {"success": True, "message": "Feedback submitted"}, 201
