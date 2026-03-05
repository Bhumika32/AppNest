from datetime import datetime
from app.core.extensions import db

class UserProgression(db.Model):
    """
    Model for tracking universal user progression.
    """
    __tablename__ = 'user_progression'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    total_xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    rank_title = db.Column(db.String(100), default="Apprentice")
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = db.relationship('User', backref=db.backref('progression', uselist=False, lazy=True))

    def to_dict(self):
        # We need xp_required for next level for frontend display logic ideally.
        # But for model dict, just return raw fields.
        return {
            "user_id": self.user_id,
            "total_xp": self.total_xp,
            "level": self.level,
            "rank_title": self.rank_title,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
