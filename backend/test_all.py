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
    
    # 1. Simulate GameEngine payload for tic-tac-toe
    print("Testing TicTacToe...")
    exec_url_tt = "http://127.0.0.1:5000/api/modules/execute/tic-tac-toe"
    payload_tt = {
        "module_id": 2, 
        "duration": 15, 
        "score": 100, 
        "difficulty": "EASY", 
        "result": "win", 
        "metadata": {"turns": 5}
    }
    res = requests.post(exec_url_tt, json=payload_tt, headers=headers)
    print("TicTacToe Status:", res.status_code)
    print("Response:", res.text)

    # 2. Simulate ToolLayout payload for currency-converter
    print("\nTesting Currency Converter...")
    exec_url_cc = "http://127.0.0.1:5000/api/modules/execute/currency-converter"
    payload_cc = {
        "module_id": 14, 
        "duration": 5, 
        "score": 50, 
        "difficulty": "EASY", 
        "result": "completed", 
        "metadata": {"amount": "100", "from": "USD", "to": "EUR"}
    }
    res = requests.post(exec_url_cc, json=payload_cc, headers=headers)
    print("Currency Status:", res.status_code)
    print("Response:", res.text)
