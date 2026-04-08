import os
import sys

# Ensure we're running from the backend directory
sys.path.insert(0, os.path.abspath('.'))

from app import create_app
from sqlalchemy.orm import Session
from app.domain.lifecycle_service import LifecycleService
#from app.domain.progression_service import ProgressionService
from app.models.user import User

app = create_app()

print("--- STARTING VALIDATION ---")

with app.app_context():
    db: Session = app.extensions['db'].session  
    # Setup test user
    user = User.query.filter_by(email="test@appnest.com").first()
    if not user:
        user = User(email="test@appnest.com", username="tester", is_verified=True)
        user.set_password("password123")
        db.add(user)
        db.commit()
    
    user_id = user.id
    
    print("1. Backend Context Loaded Successfully")
    
    print("\n2. Executing Game (Tic Tac Toe)")
    try:
        res = LifecycleService.execute_module(user_id, "tic-tac-toe", {"difficulty": "EASY"}, entry_id=None)
        
        # We manually call complete module as if the game ended with a win
        lifecycle_res = LifecycleService.complete_module(user_id, {
            "module_id": res['module']['id'],
            "module_slug": "tic-tac-toe",
            "score": 100,
            "duration": 30,
            "difficulty": "EASY",
            "result": "win",
            "metadata": {},
            "input": {}
        })
        print(f"Game XP Rewarded: {lifecycle_res['xp_reward']['xp_awarded']}")
        print(f"Current Level: {lifecycle_res['xp_reward']['level']}")
    except Exception as e:
        print(f"Failed Game Execution: {e}")
        
    print("\n3. Executing Tool (BMI Calculator)")
    try:
        res = LifecycleService.execute_module(user_id, "bmi-calculator", {"input": {"weight": 70, "height": 175}}, entry_id=None)
        
        # Tool completion
        lifecycle_res = LifecycleService.complete_module(user_id, {
            "module_id": res['module']['id'],
            "module_slug": "bmi-calculator",
            "score": 100,
            "duration": 10,
            "difficulty": "EASY",
            "result": "completed",
            "metadata": {},
            "input": {"weight": 70, "height": 175}
        })
        print(f"Tool XP Rewarded: {lifecycle_res['xp_reward']['xp_awarded']}")
        
        # executing again to test deduplication
        lifecycle_res2 = LifecycleService.complete_module(user_id, {
            "module_id": res['module']['id'],
            "module_slug": "bmi-calculator",
            "score": 100,
            "duration": 10,
            "difficulty": "EASY",
            "result": "completed",
            "metadata": {},
            "input": {"weight": 70, "height": 175}
        })
        print(f"Tool XP Rewarded (Duplicate): {lifecycle_res2['xp_reward']['xp_awarded']}")
    except Exception as e:
        print(f"Failed Tool Execution: {e}")

print("\n--- VALIDATION COMPLETE ---")
