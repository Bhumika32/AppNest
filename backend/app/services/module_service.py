from typing import List, Optional, Tuple
from app.core.extensions import db
from app.models.module import Module, ModuleAnalytics

class ModuleService:
    @staticmethod
    def get_all_modules(type_filter: Optional[str] = None) -> List[Module]:
        query = Module.query.filter_by(is_active=True)
        if type_filter:
            query = query.filter_by(type=type_filter)
        return query.all()

    @staticmethod
    def get_module_by_slug(slug: str) -> Optional[Module]:
        return Module.query.filter_by(slug=slug, is_active=True).first()

    @staticmethod
    def track_module_start(user_id: int, module_id: int) -> ModuleAnalytics:
        entry = ModuleAnalytics(user_id=user_id, module_id=module_id, event_type='start')
        db.session.add(entry)
        db.session.commit()
        return entry

    @staticmethod
    def track_module_end(user_id: int, entry_id: int, duration: int) -> Tuple[bool, str]:
        entry = ModuleAnalytics.query.get(entry_id)
        if entry and entry.user_id == int(user_id):
            entry.event_type = 'end'
            entry.duration = duration
            db.session.commit()
            return True, "Session finalized"
        return False, "Invalid entry"

    @staticmethod
    def create_module(data: dict) -> Module:
        new_module = Module(
            name=data.get('name'),
            type=data.get('type'),
            slug=data.get('slug'),
            description=data.get('description'),
            icon=data.get('icon'),
            thumbnail=data.get('thumbnail'),
            component_key=data.get('component_key'),
            category=data.get('category'),
            difficulty=data.get('difficulty'),
            is_active=data.get('is_active', True)
        )
        db.session.add(new_module)
        db.session.commit()
        return new_module

    @staticmethod
    def update_module(module_id: int, data: dict) -> Optional[Module]:
        module = Module.query.get(module_id)
        if not module:
            return None
            
        for key, value in data.items():
            if hasattr(module, key):
                setattr(module, key, value)
                
        db.session.commit()
        return module

    @staticmethod
    def delete_module(module_id: int) -> bool:
        module = Module.query.get(module_id)
        if not module:
            return False
        db.session.delete(module)
        db.session.commit()
        return True
