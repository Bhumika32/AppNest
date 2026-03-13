"""
app/models/notification.py

User notification model for storing persistent notifications in database.
Supports multiple notification types for a complete notification center.
"""

from datetime import datetime
from app.core.extensions import db


class Notification(db.Model):
    """
    User Notification Model
    
    Types: 
      - 'achievement': User unlocked an achievement
      - 'game': Game result/stats related
      - 'credit': Credit awarded (game win, tool completion)
      - 'system': System announcements or maintenance
      - 'social': Friend activity, leaderboard, mentions
      - 'alert': Important alerts or updates
    """
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    type = db.Column(db.String(50), nullable=False, default='info')  # notification type
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    read = db.Column(db.Boolean, default=False, index=True)
    read_at = db.Column(db.DateTime, nullable=True)
    data = db.Column(db.JSON, nullable=True)  # Extra context (e.g., game_id, achievement_id)
    action_url = db.Column(db.String(255), nullable=True)  # Where to navigate on click
    icon = db.Column(db.String(50), nullable=True)  # Icon name (lucide-react)
    color = db.Column(db.String(50), nullable=True)  # Color class (neon-blue, neon-pink, etc.)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    expires_at = db.Column(db.DateTime, nullable=True)  # Auto-delete after this time
    
    # Relationships
    user = db.relationship('User', backref=db.backref('notifications', cascade='all, delete-orphan'))

    def to_dict(self):
        """Convert notification to frontend-safe dictionary."""

        return {
            "id": self.id,
            "type": self.type,
            "title": self.title,
            "message": self.message,

            # frontend contract
            "seen": self.read,
            "timestamp": self.created_at.isoformat(),

            "icon": self.icon,
            "color": self.color,
            "data": self.data,
            "action_url": self.action_url,

            "read_at": self.read_at.isoformat() if self.read_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None
        }

    def mark_as_read(self):
        """Mark notification as read."""
        self.read = True
        self.read_at = datetime.utcnow()

    def __repr__(self):
        return f'<Notification {self.id} - {self.type} - {self.title}>'
