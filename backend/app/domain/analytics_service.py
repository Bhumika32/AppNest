from app.models.module import Module, ModuleAnalytics
from app.models.user import User
from app.core.extensions import db
from datetime import datetime, timedelta
from sqlalchemy import func

class AnalyticsService:
    @staticmethod
    def get_platform_stats():
        """Aggregates real stats from the database."""
        active_users = User.query.filter_by(is_verified=True).count()
        
        # Today's activity
        today = datetime.utcnow().date()
        total_sessions = ModuleAnalytics.query.filter(
            func.date(ModuleAnalytics.timestamp) == today
        ).count()

        # Growth trend (simplified: compare this week to last week)
        last_week = datetime.utcnow() - timedelta(days=7)
        new_users_week = User.query.filter(User.created_at >= last_week).count()
        
        return {
            "activeUsers": active_users,
            "matchesToday": total_sessions,
            "toolUsage": total_sessions, # Combined for now
            "roastBattles": 0, # Placeholder until RoastAnalytics exists
            "systemHealth": "optimal",
            "growthTrend": round((new_users_week / (active_users or 1)) * 100, 1)
        }

    @staticmethod
    def get_user_growth_data():
        """Returns time-series user growth from DB using a single aggregated query."""
        fourteen_days_ago = datetime.utcnow().date() - timedelta(days=13)
        
        # Determine total users before the 14-day window
        base_count = User.query.filter(func.date(User.created_at) < fourteen_days_ago).count()
        
        # Group new users by day
        daily_new_users = db.session.query(
            func.date(User.created_at).label('day'),
            func.count(User.id).label('new_users')
        ).filter(func.date(User.created_at) >= fourteen_days_ago).group_by('day').all()
        
        new_users_by_day = {str(day): count for day, count in daily_new_users}
        
        data = []
        current_total = base_count
        
        for i in range(14):
            day = fourteen_days_ago + timedelta(days=i)
            day_str = day.strftime('%Y-%m-%d')
            new_users = new_users_by_day.get(day_str, 0)
            current_total += new_users
            
            data.append({
                "date": day_str,
                "users": current_total,
                "retention": 85, # Default placeholder
                "newUsers": new_users
            })
        return data

    @staticmethod
    def get_game_popularity():
        """Returns sessions per game module."""
        results = db.session.query(
            Module.name, 
            func.count(ModuleAnalytics.id).label('sessions')
        ).join(ModuleAnalytics).filter(Module.type == 'game').group_by(Module.id).all()
        
        return [{"name": r[0], "sessions": r[1], "active": 0, "rating": 5.0} for r in results] or [
            {"name": "No Games Active", "sessions": 0, "active": 0, "rating": 0}
        ]

    @staticmethod
    def get_tool_usage():
        """Returns usage per tool module."""
        results = db.session.query(
            Module.name, 
            func.count(ModuleAnalytics.id).label('usage')
        ).join(ModuleAnalytics).filter(Module.type == 'tool').group_by(Module.id).all()
        
        return [{"name": r[0], "usage": r[1]} for r in results] or [
            {"name": "No Tools Active", "usage": 0}
        ]
