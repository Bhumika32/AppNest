from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import logging

from app.core.cache_service import CacheService
from app.repositories.analytics_repository import AnalyticsRepository

logger = logging.getLogger(__name__)

class AnalyticsService:

    def get_analytics_repository():
        return AnalyticsRepository()

    @staticmethod
    def get_platform_stats(db: Session):
        cache_key = "app:analytics:platform_stats"
        cached = CacheService.get_json(cache_key)
        if cached: return cached

        try:
            active_users = AnalyticsRepository().get_active_users_count(db)
            start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            end = start + timedelta(days=1)

            total_sessions = AnalyticsRepository().get_total_sessions_in_range(db, start, end)
            tool_usage = AnalyticsRepository().get_tool_usage_in_range(db, start, end)

            now = datetime.utcnow()
            this_week_start = now - timedelta(days=7)
            last_week_start = now - timedelta(days=14)

            this_week_users = AnalyticsRepository().get_user_count_in_range(db, this_week_start)
            last_week_users = AnalyticsRepository().get_user_count_in_range(db, last_week_start, this_week_start)

            growth = 0
            if last_week_users > 0: growth = ((this_week_users - last_week_users) / last_week_users) * 100

            result = {
                "activeUsers": active_users,
                "matchesToday": total_sessions,
                "toolUsage": tool_usage,
                "roastBattles": 0,
                "systemHealth": "optimal",
                "growthTrend": round(growth, 2)
            }
            CacheService.set_json(cache_key, result, ex=60)
            return result
        except Exception as e:
            logger.error(f"Analytics error: {e}")
            return {}

    @staticmethod
    def get_user_growth_data(db: Session):
        cache_key = "app:analytics:user_growth"
        cached = CacheService.get_json(cache_key)
        if cached: return cached

        try:
            start_date = datetime.utcnow().date() - timedelta(days=13)
            results = AnalyticsRepository().get_user_growth_by_day(db, start_date)
            data_map = {str(r[0]): r[1] for r in results}

            data = []
            total = 0
            for i in range(14):
                day = start_date + timedelta(days=i)
                day_str = day.strftime('%Y-%m-%d')
                new_users = data_map.get(day_str, 0)
                total += new_users
                data.append({"date": day_str, "users": total, "newUsers": new_users})

            CacheService.set_json(cache_key, data, ex=300)
            return data
        except Exception as e:
            logger.error(f"User growth error: {e}")
            return []

    @staticmethod
    def get_game_popularity(db: Session):
        cache_key = "app:analytics:games"
        cached = CacheService.get_json(cache_key)
        if cached: return cached

        try:
            results = AnalyticsRepository().get_module_popularity(db, "game")
            data = [{"name": r[0], "sessions": r[1]} for r in results]
            CacheService.set_json(cache_key, data, ex=300)
            return data
        except Exception as e:
            logger.error(f"Game popularity error: {e}")
            return []

    @staticmethod
    def get_tool_usage(db: Session):
        cache_key = "app:analytics:tools"
        cached = CacheService.get_json(cache_key)
        if cached: return cached

        try:
            results = AnalyticsRepository().get_module_popularity(db, "tool")
            data = [{"name": r[0], "usage": r[1]} for r in results]
            CacheService.set_json(cache_key, data, ex=300)
            return data
        except Exception as e:
            logger.error(f"Tool usage error: {e}")
            return []

    @staticmethod
    def get_engagement_stats(db: Session):
        return {
            "dailyActiveUsers": 0,
            "sessionDuration": "0m",
            "retentionRate": "0%",
            "topModules": []
        }
