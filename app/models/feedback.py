"""
app/models/feedback.py

Database model for storing user feedback.

Purpose:
- Allows logged-in users to submit feedback about the application
- Supports star rating (1 to 5) and a message
- Stores timestamp for audit/history

Table: feedback
"""

from datetime import datetime
from app.extensions import db


class Feedback(db.Model):
    """
    Feedback table model.

    Fields:
    - id: Primary key
    - user_id: Foreign reference to users.id (we keep it as int for simplicity)
    - rating: Rating score between 1 and 5
    - message: Feedback text from user
    - created_at: Timestamp when feedback is created
    """

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True)

    # Note:
    # We store user_id as an Integer here.
    # You can also add db.ForeignKey("users.id") later for strict relation.
    user_id = db.Column(db.Integer, nullable=False)

    rating = db.Column(db.Integer, nullable=False)  # Expected: 1 to 5
    message = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        """Developer-friendly representation for debugging."""
        return f"<Feedback id={self.id} user_id={self.user_id} rating={self.rating}>"