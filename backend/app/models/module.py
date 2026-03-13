from datetime import datetime
from app.core.extensions import db

class Module(db.Model):
    """
    Model for dynamic apps (tools and games) behaves like plugins.
    """
    __tablename__ = 'modules'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # "game" | "tool"
    slug = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))  # Emoji or lucide icon name
    thumbnail = db.Column(db.String(255))
    component_key = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))
    difficulty = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)
    capabilities = db.Column(db.JSON, nullable=True)
    xp_reward_base = db.Column(db.Integer, default=10)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "slug": self.slug,
            "description": self.description,
            "icon": self.icon,
            "thumbnail": self.thumbnail,
            "component_key": self.component_key,
            "category": self.category,
            "difficulty": self.difficulty,
            "is_active": self.is_active,
            "capabilities": self.capabilities,
            "xp_reward_base": self.xp_reward_base,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class ModuleAnalytics(db.Model):
    """
    Tracks usage metrics for specific modules.
    """
    __tablename__ = 'module_analytics'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id'), nullable=False)
    event_type = db.Column(db.String(50)) # 'start', 'end'
    duration = db.Column(db.Integer, default=0) # in seconds
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', backref=db.backref('module_analytics', lazy=True))
    module = db.relationship('Module', backref=db.backref('analytics', lazy=True))
