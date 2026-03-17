from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.models.module import Module, ModuleAnalytics
from app.models.user import User
from app.core.redis_client import neural_cache


class AnalyticsService:

    @staticmethod
    def get_platform_stats(db: Session):
        cache_key = "analytics:platform_stats"

        cached = neural_cache.get(cache_key)
        if cached:
            return cached

        active_users = db.query(User).filter(User.is_verified == True).count()

        start = datetime.utcnow().replace(hour=0, minute=0, second=0)
        end = start + timedelta(days=1)

        total_sessions = db.query(ModuleAnalytics).filter(
            ModuleAnalytics.timestamp >= start,
            ModuleAnalytics.timestamp < end
        ).count()

        tool_usage = db.query(ModuleAnalytics).join(Module).filter(
            Module.type == "tool",
            ModuleAnalytics.timestamp >= start,
            ModuleAnalytics.timestamp < end
        ).count()

        now = datetime.utcnow()
        this_week_start = now - timedelta(days=7)
        last_week_start = now - timedelta(days=14)

        this_week_users = db.query(User).filter(
            User.created_at >= this_week_start
        ).count()

        last_week_users = db.query(User).filter(
            User.created_at >= last_week_start,
            User.created_at < this_week_start
        ).count()

        growth = 0
        if last_week_users > 0:
            growth = ((this_week_users - last_week_users) / last_week_users) * 100

        result = {
            "activeUsers": active_users,
            "matchesToday": total_sessions,
            "toolUsage": tool_usage,
            "roastBattles": 0,
            "systemHealth": "optimal",
            "growthTrend": round(growth, 2)
        }

        neural_cache.set(cache_key, result, ex=60)

        return result

    @staticmethod
    def get_user_growth_data(db: Session):
        cache_key = "analytics:user_growth"

        cached = neural_cache.get(cache_key)
        if cached:
            return cached

        start_date = datetime.utcnow().date() - timedelta(days=13)

        results = db.query(
            func.date(User.created_at).label("day"),
            func.count(User.id)
        ).filter(
            User.created_at >= start_date
        ).group_by("day").all()

        data_map = {str(r[0]): r[1] for r in results}

        data = []
        total = 0

        for i in range(14):
            day = start_date + timedelta(days=i)
            day_str = day.strftime('%Y-%m-%d')

            new_users = data_map.get(day_str, 0)
            total += new_users

            data.append({
                "date": day_str,
                "users": total,
                "newUsers": new_users
            })

        neural_cache.set(cache_key, data, ex=300)

        return data

    @staticmethod
    def get_game_popularity(db: Session):
        cache_key = "analytics:games"

        cached = neural_cache.get(cache_key)
        if cached:
            return cached

        results = db.query(
            Module.name,
            func.count(ModuleAnalytics.id)
        ).join(ModuleAnalytics).filter(
            Module.type == "game"
        ).group_by(Module.id).all()

        data = [
            {"name": r[0], "sessions": r[1]}
            for r in results
        ]

        neural_cache.set(cache_key, data, ex=300)

        return data

    @staticmethod
    def get_tool_usage(db: Session):
        cache_key = "analytics:tools"

        cached = neural_cache.get(cache_key)
        if cached:
            return cached

        results = db.query(
            Module.name,
            func.count(ModuleAnalytics.id)
        ).join(ModuleAnalytics).filter(
            Module.type == "tool"
        ).group_by(Module.id).all()

        data = [
            {"name": r[0], "usage": r[1]}
            for r in results
        ]

        neural_cache.set(cache_key, data, ex=300)

        return data

# from app.models.module import Module, ModuleAnalytics
# from app.models.user import User
# from sqlalchemy.orm import Session
# from app.core.database import get_db
# from datetime import datetime, timedelta
# from sqlalchemy import func

# class AnalyticsService:
#     @staticmethod
#     def get_platform_stats(db: Session):
#         """Aggregates real stats from the database."""
#         active_users = db.query(User).filter_by(is_verified=True).count()
        
#         # Today's activity
#         today = datetime.utcnow().date()
#         total_sessions = ModuleAnalytics.query.filter(
#             func.date(ModuleAnalytics.timestamp) == today
#         ).count()

#         # Growth trend (simplified: compare this week to last week)
#         last_week = datetime.utcnow() - timedelta(days=7)
#         new_users_week = User.query.filter(User.created_at >= last_week).count()
        
#         return {
#             "activeUsers": active_users,
#             "matchesToday": total_sessions,
#             "toolUsage": total_sessions, # Combined for now
#             "roastBattles": 0, # Placeholder until RoastAnalytics exists
#             "systemHealth": "optimal",
#             "growthTrend": round((new_users_week / (active_users or 1)) * 100, 1)
#         }

#     @staticmethod
#     def get_user_growth_data(
#         db: Session
#     ):
#         """Returns time-series user growth from DB using a single aggregated query."""
#         fourteen_days_ago = datetime.utcnow().date() - timedelta(days=13)
        
#         # Determine total users before the 14-day window
#         base_count = db.query(User).filter(
#             func.date(User.created_at) < fourteen_days_ago
#         ).count()
        
#         # Group new users by day
#         daily_new_users = db.query(
#             func.date(User.created_at).label('day'),
#             func.count(User.id).label('new_users')
#         ).filter(func.date(User.created_at) >= fourteen_days_ago).group_by('day').all()
        
#         new_users_by_day = {str(day): count for day, count in daily_new_users}
        
#         data = []
#         current_total = base_count
        
#         for i in range(14):
#             day = fourteen_days_ago + timedelta(days=i)
#             day_str = day.strftime('%Y-%m-%d')
#             new_users = new_users_by_day.get(day_str, 0)
#             current_total += new_users
            
#             data.append({
#                 "date": day_str,
#                 "users": current_total,
#                 "retention": 85, # Default placeholder
#                 "newUsers": new_users
#             })
#         return data

#     @staticmethod
#     def get_game_popularity(db: Session):
#         """Returns sessions per game module."""
#         results = db.query(
#             Module.name, 
#             func.count(ModuleAnalytics.id).label('sessions')
#         ).join(ModuleAnalytics).filter(Module.type == 'game').group_by(Module.id).all()
        
#         return [{"name": r[0], "sessions": r[1], "active": 0, "rating": 5.0} for r in results] or [
#             {"name": "No Games Active", "sessions": 0, "active": 0, "rating": 0}
#         ]

#     @staticmethod
#     def get_tool_usage(db: Session):
#         """Returns usage per tool module."""
#         results = db.query(
#             Module.name, 
#             func.count(ModuleAnalytics.id).label('usage')
#         ).join(ModuleAnalytics).filter(Module.type == 'tool').group_by(Module.id).all()
        
#         return [{"name": r[0], "usage": r[1]} for r in results] or [
#             {"name": "No Tools Active", "usage": 0}
#         ]
