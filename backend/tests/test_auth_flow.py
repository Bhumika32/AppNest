"""Test the auth flow end-to-end"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

# Test 1: Register new user
print("\n=== TEST 1: Register New User ===")
signup_payload = {
    "email": "testuser@example.com",
    "username": "testuser123",
    "password": "SecurePass123!",
    "confirm_password": "SecurePass123!"
}
signup_response = requests.post(f"{BASE_URL}/api/auth/register", json=signup_payload)
print(f"Status: {signup_response.status_code}")
print(f"Response: {json.dumps(signup_response.json(), indent=2)}")

if signup_response.status_code == 201:
    # Test 2: Login with new user
    print("\n=== TEST 2: Login ===")
    login_payload = {
        "email": "testuser@example.com",
        "password": "SecurePass123!"
    }
    login_response = requests.post(f"{BASE_URL}/api/auth/login", json=login_payload)
    print(f"Status: {login_response.status_code}")
    print(f"Response: {json.dumps(login_response.json(), indent=2)}")
    
    if login_response.status_code == 200:
        tokens = login_response.json().get('data', {})
        access_token = tokens.get('access_token')
        print(f"\n✓ Received JWT access_token: {access_token[:50]}...")
        
        # Test 3: Access protected endpoint
        print("\n=== TEST 3: Access Protected Endpoint ===")
        headers = {"Authorization": f"Bearer {access_token}"}
        protected_response = requests.get(f"{BASE_URL}/api/main/dashboard", headers=headers)
        print(f"Status: {protected_response.status_code}")
        print(f"Response: {json.dumps(protected_response.json(), indent=2)}")
        
        if protected_response.status_code == 200:
            print("\n✓✓✓ AUTH FLOW SUCCESSFUL ✓✓✓")
        else:
            print("\n✗ Failed to access protected endpoint")
    else:
        print("\n✗ Login failed")
else:
    print("\n✗ Signup failed")
