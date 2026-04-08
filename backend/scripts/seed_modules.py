"""
Production-grade module seeder

✔ Idempotent
✔ Clean architecture
✔ Fully aligned with executors + frontend
✔ Supports capabilities (modes, difficulty)
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.database import SessionLocal
from app.models.module import Module


def seed_modules():
    db = SessionLocal()

    modules = [

        # -----------------------------
        # 🧠 TOOLS
        # -----------------------------

        {
            "name": "BMI Calculator",
            "type": "tool",
            "slug": "bmi-calculator",
            "component_key": "BMICalculator",
            "description": "Precision body mass index calculator.",
            "icon": "⚖️",
            "category": "health",
            "difficulty": "Simple",
            "xp_reward_base": 30,
            "capabilities": {"requiresSetup": False},
            "is_active": True,
        },

        {
            "name": "Currency Converter",
            "type": "tool",
            "slug": "currency-converter",
            "component_key": "CurrencyConverter",
            "description": "Convert currencies in real-time.",
            "icon": "💱",
            "category": "finance",
            "difficulty": "Simple",
            "xp_reward_base": 20,
            "capabilities": {"requiresSetup": False},
            "is_active": True,
        },

        {
            "name": "Age Calculator",
            "type": "tool",
            "slug": "age-calculator",
            "component_key": "AgeCalculator",
            "description": "Advanced age insights with personality analysis.",
            "icon": "🎂",
            "category": "utility",
            "difficulty": "Simple",
            "xp_reward_base": 25,
            "capabilities": {"requiresSetup": False,},
            "is_active": True,
        },

        {
            "name": "Unit Converter",
            "type": "tool",
            "slug": "unit-converter",
            "component_key": "UnitConverter",
            "description": "Convert units across multiple categories.",
            "icon": "📏",
            "category": "utility",
            "difficulty": "Simple",
            "xp_reward_base": 20,
            "capabilities": {"requiresSetup": False},
            "is_active": True,
        },

        {
            "name": "Weather Tool",
            "type": "tool",
            "slug": "weather",
            "component_key": "WeatherTool",
            "description": "Real-time weather forecasting.",
            "icon": "🌦️",
            "category": "utility",
            "difficulty": "Simple",
            "xp_reward_base": 15,
            "capabilities": {"requiresSetup": False},
            "is_active": True,
        },

        {
            "name": "Translator",
            "type": "tool",
            "slug": "translator",
            "component_key": "TranslatorTool",
            "description": "Translate text instantly.",
            "icon": "🌐",
            "category": "utility",
            "difficulty": "Simple",
            "xp_reward_base": 15,
            "capabilities": {"requiresSetup": False},
            "is_active": True,
        },

        {
            "name": "Joke Generator",
            "type": "tool",
            "slug": "joke",
            "component_key": "JokeGenerator",
            "description": "Generate programming jokes.",
            "icon": "😂",
            "category": "fun",
            "difficulty": "Simple",
            "xp_reward_base": 5,
            "capabilities": {"requiresSetup": False},
            "is_active": True,
        },

        {
            "name": "Rashi Generator",
            "type": "tool",
            "slug": "rashi",
            "component_key": "RashiGenerator",
            "description": "Zodiac personality insights.",
            "icon": "🔮",
            "category": "fun",
            "difficulty": "Simple",
            "xp_reward_base": 10,
            "capabilities": {"requiresSetup": False},
            "is_active": True,
        },

        {
            "name": "CGPA Calculator",
            "type": "tool",
            "slug": "cgpa",
            "component_key": "CGPACalculator",
            "description": "Calculate academic CGPA.",
            "icon": "🎓",
            "category": "education",
            "difficulty": "Simple",
            "xp_reward_base": 20,
            "capabilities": {"requiresSetup": False},
            "is_active": True,
        },

        # -----------------------------
        # 🎮 GAMES (BACKEND CONTROLLED)
        # -----------------------------

        {
            "name": "Tic Tac Toe",
            "type": "game",
            "slug": "tic-tac-toe",
            "component_key": "TicTacToeGame",
            "description": "Classic strategy game with AI.",
            "icon": "❌",
            "category": "logic",
            "difficulty": "Easy",
            "xp_reward_base": 50,
            "capabilities": {
            "requiresSetup": True,
            "modes": ["solo", "vs_ai"],
            "difficulty_levels": ["easy", "medium", "hard"]
            },
            "is_active": True,
        },

        {
            "name": "Snake Game",
            "type": "game",
            "slug": "snake-game",
            "component_key": "SnakeGame",
            "description": "Classic snake survival game.",
            "icon": "🐍",
            "category": "arcade",
            "difficulty": "Medium",
            "xp_reward_base": 60,
            "capabilities": {
                "requiresSetup": True,
                "difficulty_levels": ["easy", "medium", "hard"]
            },
            "is_active": True,
        },

        {
            "name": "Flappy Bird",
            "type": "game",
            "slug": "flappy-bird",
            "component_key": "FlappyBirdGame",
            "description": "High reflex flying game.",
            "icon": "🐦",
            "category": "arcade",
            "difficulty": "Hard",
            "xp_reward_base": 70,
            "capabilities": {
                "requiresSetup": True,
                "difficulty_levels": ["easy", "medium", "hard", "extreme"]
            },
            "is_active": True,
        },

        {
            "name": "Brick Breaker",
            "type": "game",
            "slug": "brick-breaker",
            "component_key": "BrickBreakerGame",
            "description": "Break bricks and level up.",
            "icon": "🧱",
            "category": "arcade",
            "difficulty": "Medium",
            "xp_reward_base": 80,
            "capabilities": {
                "requiresSetup": True,
                "difficulty_levels": ["easy", "medium", "hard"]
            },
            "is_active": True,
        },
    ]

    added, updated = 0, 0

    try:
        for data in modules:
            existing = db.query(Module).filter(Module.slug == data["slug"]).first()

            if existing:
                changed = False
                for key, value in data.items():
                    if getattr(existing, key) != value:
                        setattr(existing, key, value)
                        changed = True

                if changed:
                    updated += 1
                    print(f"[UPDATED] {data['name']}")
                else:
                    print(f"[SKIPPED] {data['name']}")

            else:
                db.add(Module(**data))
                added += 1
                print(f"[ADDED] {data['name']}")

        db.commit()
        print(f"\n✅ DONE → Added: {added}, Updated: {updated}")

    except Exception as e:
        db.rollback()
        print("❌ ERROR:", str(e))

    finally:
        db.close()


if __name__ == "__main__":
    seed_modules()