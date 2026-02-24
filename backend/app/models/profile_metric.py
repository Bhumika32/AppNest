from datetime import datetime
from app.core.extensions import db


class ProfileMetric(db.Model):
    __tablename__ = 'profile_metrics'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    key = db.Column(db.String(120), nullable=False)
    value = db.Column(db.String(255), nullable=False)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<ProfileMetric id={self.id} user_id={self.user_id} key={self.key} value={self.value}>"
