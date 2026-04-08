# app/repositories/module_repository.py

"""
Module Repository (Stateless)

✔ Clean filtering
✔ Stable ordering
"""

from typing import Optional, List
from sqlalchemy.orm import Session

from app.models.module import Module
from app.repositories.base_repository import BaseRepository


class ModuleRepository(BaseRepository[Module]):

    def __init__(self):
        super().__init__(Module)

    def get_active_by_slug(self, db: Session, slug: str) -> Optional[Module]:
        return db.query(self.model).filter(
            self.model.slug == slug,
            self.model.is_active.is_(True)
        ).first()

    def get_all_active(self, db: Session, type_filter: Optional[str] = None) -> List[Module]:
        query = db.query(self.model).filter(self.model.is_active.is_(True))

        if type_filter:
            query = query.filter(self.model.type == type_filter)

        return query.order_by(self.model.id.asc()).all()
# from typing import Optional, List
# from sqlalchemy.orm import Session
# from app.models.module import Module
# from app.repositories.base_repository import BaseRepository

# class ModuleRepository(BaseRepository[Module]):
#     def __init__(self):
#         super().__init__(Module)

#     def get_active_by_slug(self, db: Session, slug: str) -> Optional[Module]:
#         return db.query(self.model).filter(
#             self.model.slug == slug,
#             self.model.is_active.is_(True)
#         ).first()

#     def get_all_active(self, db: Session, type_filter: Optional[str] = None) -> List[Module]:
#         query = db.query(self.model).filter(self.model.is_active.is_(True))
#         if type_filter:
#             query = query.filter_by(type=type_filter)
#         return query.all()


