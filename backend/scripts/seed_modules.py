import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.core.extensions import db
from app.models.module import Module

def seed_modules():
    app = create_app()
    with app.app_context():
        # Clear existing to avoid unique constraint errors during dev
        # db.session.query(Module).delete()
        
        modules = [
            {
                "name": "BMI Calculator",
                "type": "tool",
                "slug": "bmi-calculator",
                "description": "Precision body mass index calibration for neural physicals.",
                "icon": "⚖️",
                "component_key": "BMICalculator",
                "category": "health",
                "difficulty": "Simple"
            },
            {
                "name": "Tic Tac Toe",
                "type": "game",
                "slug": "tic-tac-toe",
                "description": "Retro-futuristic logic combat versus AI or local agents.",
                "icon": "❌",
                "component_key": "TicTacToeGame",
                "category": "logic",
                "difficulty": "Easy"
            },
            {
                "name": "Currency Converter",
                "type": "tool",
                "slug": "currency-converter",
                "description": "Real-time global currency synthesis and exchange mapping.",
                "icon": "💱",
                "component_key": "CurrencyConverter",
                "category": "finance",
                "difficulty": "Simple"
            }
        ]

        for m_data in modules:
            existing = Module.query.filter_by(slug=m_data['slug']).first()
            if not existing:
                mod = Module(**m_data)
                db.add(mod)
                print(f"Adding module: {m_data['name']}")
            else:
                print(f"Module {m_data['name']} already exists. Skipping.")

        db.commit()
        print("Neural Module seeding complete.")

if __name__ == "__main__":
    seed_modules()
