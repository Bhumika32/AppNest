from typing import Generic, TypeVar, Type, Optional, List, Any
from sqlalchemy.orm import Session
from app.core.database import Base

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get_by_id(self, db: Session, id) -> Optional[ModelType]:
        return db.get(self.model, id)

    def create(self, db: Session, obj_in: dict) -> ModelType:
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.flush()  #  ensures ID is generated
        return db_obj

    def update(self, db: Session, db_obj: ModelType, obj_in: dict) -> ModelType:
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        db.flush()
        return db_obj

    def delete(self, db: Session, id) -> bool:
        obj = self.get_by_id(db, id)
        if obj:
            db.delete(obj)
            db.flush()
            return True
        return False