from app.core.extensions import db
from datetime import datetime

class Quest(db.Model):
    __tablename__ = 'quests'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    module_key = db.Column(db.String(50)) # e.g., 'flappy-bird' or 'bmi-calculator'
    target_score = db.Column(db.Integer, default=0)
    xp_reward = db.Column(db.Integer, default=50)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "module_key": self.module_key,
            "target_score": self.target_score,
            "xp_reward": self.xp_reward,
            "is_active": self.is_active
        }

class UserQuest(db.Model):
    __tablename__ = 'user_quests'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quest_id = db.Column(db.Integer, db.ForeignKey('quests.id'), nullable=False)
    status = db.Column(db.String(20), default='PENDING') # PENDING, COMPLETED, FAILED
    progress = db.Column(db.Integer, default=0)
    completed_at = db.Column(db.DateTime)
    
    quest = db.relationship('Quest', backref='user_participations')

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "quest": self.quest.to_dict() if self.quest else None,
            "status": self.status,
            "progress": self.progress,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }
