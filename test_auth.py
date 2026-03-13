import requests

try:
    resp = requests.post(
        "http://localhost:5000/api/auth/login",
        json={"email": "admin@appnest.com", "password": "password123"}
    )
    print("Status:", resp.status_code)
    print("Body:", resp.text)
    print("Cookies:", resp.cookies.get_dict())
except Exception as e:
    print("Error:", e)
