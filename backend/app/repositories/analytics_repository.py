# app/repositories/analytics_repository.py

"""
Analytics Repository (Stateless)

✔ Query optimized
✔ Clean joins
✔ Safe defaults
"""

from typing import List, Tuple, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime

from app.models.module import Module
from app.models.module_analytics import ModuleAnalytics
from app.models.user import User
from app.repositories.base_repository import BaseRepository


class AnalyticsRepository(BaseRepository[ModuleAnalytics]):

    def __init__(self):
        super().__init__(ModuleAnalytics)

    def get_active_users_count(self, db: Session) -> int:
        return db.query(func.count(User.id)).filter(User.is_verified.is_(True)).scalar() or 0

    def get_total_sessions_in_range(self, db: Session, start: datetime, end: datetime) -> int:
        return db.query(func.count(ModuleAnalytics.id)).filter(
            ModuleAnalytics.created_at >= start,
            ModuleAnalytics.created_at < end
        ).scalar() or 0

    def get_tool_usage_in_range(self, db: Session, start: datetime, end: datetime) -> int:
        return db.query(func.count(ModuleAnalytics.id))\
            .join(Module, Module.id == ModuleAnalytics.module_id)\
            .filter(
                Module.type == "tool",
                ModuleAnalytics.created_at >= start,
                ModuleAnalytics.created_at < end
            ).scalar() or 0

    def get_user_count_in_range(self, db: Session, start: datetime, end: Optional[datetime] = None) -> int:
        query = db.query(func.count(User.id)).filter(User.created_at >= start)
        if end:
            query = query.filter(User.created_at < end)
        return query.scalar() or 0

    def get_user_growth_by_day(self, db: Session, start_date: datetime) -> List[Tuple]:
        return db.query(
            func.date(User.created_at),
            func.count(User.id)
        ).filter(User.created_at >= start_date)\
         .group_by(func.date(User.created_at)).all()

    def get_module_popularity(self, db: Session, module_type: str) -> List[Tuple]:
        return db.query(
            Module.name,
            func.count(ModuleAnalytics.id)
        ).join(Module, Module.id == ModuleAnalytics.module_id)\
         .filter(Module.type == module_type)\
         .group_by(Module.id, Module.name).all()
# #backend/app/repositories/analytics_repository.py
# from typing import List, Tuple, Dict, Any, Optional
# from sqlalchemy.orm import Session
# from sqlalchemy import func
# from datetime import datetime, timedelta

# from app.models.module import Module
# from app.models.module_analytics import ModuleAnalytics
# from app.models.user import User
# from app.repositories.base_repository import BaseRepository

# class AnalyticsRepository(BaseRepository[ModuleAnalytics]):
#     def __init__(self):
#         super().__init__(ModuleAnalytics)

#     def get_active_users_count(self, db: Session) -> int:
#         return db.query(func.count(User.id)).filter(User.is_verified.is_(True)).scalar() or 0

#     def get_total_sessions_in_range(self, db: Session, start: datetime, end: datetime) -> int:
#         return db.query(func.count(ModuleAnalytics.id)).filter(
#             ModuleAnalytics.timestamp >= start,
#             ModuleAnalytics.timestamp < end
#         ).scalar() or 0

#     def get_tool_usage_in_range(self, db: Session, start: datetime, end: datetime) -> int:
#         return db.query(func.count(ModuleAnalytics.id)).select_from(ModuleAnalytics).join(
#             Module, Module.id == ModuleAnalytics.module_id
#         ).filter(
#             Module.type == "tool",
#             ModuleAnalytics.timestamp >= start,
#             ModuleAnalytics.timestamp < end
#         ).scalar() or 0

#     def get_user_count_in_range(self, db: Session, start: datetime, end: Optional[datetime] = None) -> int:
#         query = db.query(func.count(User.id)).filter(User.created_at >= start)
#         if end: query = query.filter(User.created_at < end)
#         return query.scalar() or 0

#     def get_user_growth_by_day(self, db: Session, start_date: datetime) -> List[Tuple]:
#         return db.query(
#             func.date(User.created_at),
#             func.count(User.id)
#         ).filter(User.created_at >= start_date).group_by(func.date(User.created_at)).all()

#     def get_module_popularity(self, db: Session, module_type: str) -> List[Tuple]:
#         return db.query(
#             Module.name,
#             func.count(ModuleAnalytics.id)
#         ).select_from(ModuleAnalytics).join(
#             Module, Module.id == ModuleAnalytics.module_id
#         ).filter(Module.type == module_type).group_by(Module.id).all()


