from datetime import datetime
from app.core.extensions import db

class XPTransaction(db.Model):
    """
    Model for recording individual XP awards triggered by module completions.
    """
    __tablename__ = 'xp_transactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=True) # Optional, can be null if rewarded from platform events
    xp_awarded = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.String(50), nullable=True)
    reason = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', backref=db.backref('xp_transactions', lazy=True))
    module = db.relationship('Module', backref=db.backref('xp_transactions', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "module_id": self.module_id,
            "xp_awarded": self.xp_awarded,
            "difficulty": self.difficulty,
            "reason": self.reason,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
