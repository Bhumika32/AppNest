import requests
import uuid

from app import create_app
from app.core.extensions import db
from app.models.user import User

app = create_app()

with app.app_context():
    email = f"test_{uuid.uuid4().hex[:6]}@appnest.com"
    password = "testpassword123"
    
    user = User(username=f"Test_{uuid.uuid4().hex[:6]}", email=email, is_verified=True)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    login_url = "http://127.0.0.1:5000/api/auth/login"
    res = requests.post(login_url, json={"email": email, "password": password})
    token = res.json().get("access_token")

    headers = {"Authorization": f"Bearer {token}"}
    
    # Simulate GameEngine payload for tic-tac-toe
    exec_url = "http://127.0.0.1:5000/api/modules/execute/tic-tac-toe"
    payload = {
        "module_id": 2, 
        "duration": 15, 
        "score": 100, 
        "difficulty": "EASY", 
        "result": "win", 
        "metadata": {"turns": 5}
    }
    res = requests.post(exec_url, json=payload, headers=headers)
    print("TicTacToe Status:", res.status_code)
    print("Response:", res.text)
