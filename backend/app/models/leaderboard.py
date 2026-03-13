from app.core.extensions import db
from datetime import datetime

class Leaderboard(db.Model):
    __tablename__ = 'leaderboards'
    id = db.Column(db.Integer, primary_key=True)
    module_key = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    top_score = db.Column(db.Integer, default=0)
    rank = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = db.relationship('User', backref='rankings')

    def to_dict(self):
        return {
            "id": self.id,
            "module_key": self.module_key,
            "username": self.user.username if self.user else "Unknown",
            "top_score": self.top_score,
            "rank": self.rank,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None
        }
