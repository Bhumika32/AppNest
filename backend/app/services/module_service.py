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
            is_active=data.get('is_active', True),
            capabilities=data.get('capabilities'),
            xp_reward_base=data.get('xp_reward_base', 10)
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

    @staticmethod
    def seed_modules() -> dict:
        """Seed the database with all default games and tools for the unified platform."""
        default_modules = [
            # Games
            {
                "name": "Tic Tac Toe", "type": "game", "slug": "tic-tac-toe",
                "description": "Classic logic game against AI or PvP.",
                "icon": "❌", "component_key": "TicTacToeGame", "category": "Strategy",
                "difficulty": "Dynamic", "xp_reward_base": 50,
                "capabilities": {"supportsAI": True, "supportsDifficulty": True, "supportsPVP": True, "modes": ["VS_AI", "PVP"], "difficulties": ["EASY", "MEDIUM", "HARD"]}
            },
            {
                "name": "Hungry Snake", "type": "game", "slug": "hungry-snake",
                "description": "Navigate the grid. Devour data blocks.",
                "icon": "🐍", "component_key": "SnakeGame", "category": "Arcade",
                "difficulty": "Dynamic", "xp_reward_base": 100,
                "capabilities": {"supportsDifficulty": True, "modes": ["CLASSIC"], "difficulties": ["EASY", "MEDIUM", "HARD"]}
            },
            {
                "name": "Flappy Bird", "type": "game", "slug": "flappy-bird",
                "description": "Avoid the firewall tubes to survive.",
                "icon": "🕊️", "component_key": "FlappyBirdGame", "category": "Arcade",
                "difficulty": "EASY", "xp_reward_base": 75,
                "capabilities": {"supportsDifficulty": False, "modes": ["SURVIVAL"]}
            },
            {
                "name": "Brick Breaker", "type": "game", "slug": "brick-breaker",
                "description": "Demolish the firewall layer by layer.",
                "icon": "🧱", "component_key": "BrickBreakerGame", "category": "Arcade",
                "difficulty": "MEDIUM", "xp_reward_base": 120,
                "capabilities": {"supportsDifficulty": False, "modes": ["CLASSIC"]}
            },
            # Tools
            {
                "name": "BMI Calculator", "type": "tool", "slug": "bmi-calculator",
                "description": "Calculate Body Mass Index.",
                "icon": "⚖️", "component_key": "BMICalculator", "category": "Health",
                "xp_reward_base": 30, "capabilities": {}
            },
            {
                "name": "Currency Converter", "type": "tool", "slug": "currency-converter",
                "description": "Real-time exchange rate matrix.",
                "icon": "💱", "component_key": "CurrencyConverter", "category": "Finance",
                "xp_reward_base": 30, "capabilities": {}
            },
            {
                "name": "Age Calculator", "type": "tool", "slug": "age-calculator",
                "description": "Temporal lifespan measurements.",
                "icon": "⏳", "component_key": "AgeCalculator", "category": "Utility",
                "xp_reward_base": 30, "capabilities": {}
            },
            {
                "name": "Weather Explorer", "type": "tool", "slug": "weather",
                "description": "Atmospheric readouts and forecasting.",
                "icon": "☁️", "component_key": "WeatherTool", "category": "Environment",
                "xp_reward_base": 30, "capabilities": {}
            },
            {
                "name": "Rashi Generator", "type": "tool", "slug": "rashi",
                "description": "Celestial alignment profile builder.",
                "icon": "✨", "component_key": "RashiGenerator", "category": "Utility",
                "xp_reward_base": 30, "capabilities": {}
            },
            {
                "name": "Unit Converter", "type": "tool", "slug": "unit-converter",
                "description": "Metric transformation systems.",
                "icon": "📏", "component_key": "UnitConverter", "category": "Data",
                "xp_reward_base": 30, "capabilities": {}
            },
            {
                "name": "CGPA Evaluator", "type": "tool", "slug": "cgpa",
                "description": "Compute academic index aggregates.",
                "icon": "🎓", "component_key": "CGPACalculator", "category": "Academic",
                "xp_reward_base": 30, "capabilities": {}
            },
            {
                "name": "Linguistic Decoder", "type": "tool", "slug": "translator",
                "description": "Protocol translation algorithm.",
                "icon": "🌐", "component_key": "TranslatorTool", "category": "Comms",
                "xp_reward_base": 30, "capabilities": {}
            },
            {
                "name": "Humor Synthesizer", "type": "tool", "slug": "joke",
                "description": "Generate subjective syntax errors (Jokes).",
                "icon": "🎭", "component_key": "JokeGenerator", "category": "Utility",
                "xp_reward_base": 30, "capabilities": {}
            }
        ]

        # Wipe existing hardcoded ones if needed or simply upsert
        added = 0
        updated = 0
        
        for m_data in default_modules:
            existing = Module.query.filter_by(slug=m_data["slug"]).first()
            if existing:
                for k, v in m_data.items():
                    setattr(existing, k, v)
                updated += 1
            else:
                db.session.add(Module(**m_data))
                added += 1

        db.session.commit()
        return {"added": added, "updated": updated}
