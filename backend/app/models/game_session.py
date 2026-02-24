from datetime import datetime
from app.core.extensions import db


class GameSession(db.Model):
    __tablename__ = 'game_sessions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    game_key = db.Column(db.String(80), nullable=False)
    score = db.Column(db.Integer, default=0, nullable=False)
    duration_seconds = db.Column(db.Integer, nullable=True)
    # 'metadata' is a reserved attribute name on declarative classes,
    # so expose it as `meta` while keeping the column name as 'metadata'.
    meta = db.Column('metadata', db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<GameSession id={self.id} user_id={self.user_id} game={self.game_key} score={self.score}>"
