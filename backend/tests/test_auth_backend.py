#!/usr/bin/env python
"""
Test Backend Auth Flow
Tests login and subsequent /me requests to verify admin role is returned correctly
"""

import requests
import json
from http.cookiejar import CookieJar

# Config
BACKEND_URL = "http://127.0.0.1:5000/api"
ADMIN_EMAIL = "bg226104@gmail.com"
ADMIN_PASSWORD = "password"  # Change if different

# Session to maintain cookies
session = requests.Session()

print("=" * 70)
print("AppNest Backend Auth Flow Test")
print("=" * 70)

# Step 1: Login
print(f"\n1. Logging in as {ADMIN_EMAIL}...")
try:
    login_response = session.post(
        f"{BACKEND_URL}/auth/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
        timeout=5
    )
    print(f"   Status: {login_response.status_code}")
    login_data = login_response.json()
    print(f"   Response: {json.dumps(login_data, indent=2)}")
    
    if login_response.status_code != 200:
        print("   X Login failed!")
        exit(1)
    
    access_token = login_data.get("access_token")
    user_role = login_data.get("user", {}).get("role")
    
    print(f"   - Access token: {access_token[:50]}...")
    print(f"   - User role from login: {user_role}")
    
    if user_role != "ADMIN":
        print(f"   ! WARNING: Expected 'ADMIN', got '{user_role}'")
    
except Exception as e:
    print(f"   X Error: {e}")
    exit(1)

# Step 2: Call /me endpoint with token
print(f"\n2. Calling /api/auth/me with access token...")
try:
    headers = {"Authorization": f"Bearer {access_token}"}
    me_response = session.get(
        f"{BACKEND_URL}/auth/me",
        headers=headers,
        timeout=5
    )
    print(f"   Status: {me_response.status_code}")
    me_data = me_response.json()
    print(f"   Response: {json.dumps(me_data, indent=2)}")
    
    me_role = me_data.get("role")
    print(f"   - User role from /me: {me_role}")
    
    if me_role != "ADMIN":
        print(f"   ! WARNING: Expected 'ADMIN', got '{me_role}'")
        
except Exception as e:
    print(f"   X Error: {e}")
    exit(1)

# Step 3: Check refresh token cookie
print(f"\n3. Checking HttpOnly refresh token cookie...")
try:
    cookies = session.cookies.get_dict()
    if "refresh_token" in cookies:
        print(f"   - refresh_token cookie present (HttpOnly, value hidden)")
    else:
        print(f"   ! refresh_token cookie NOT found")
        print(f"   Cookies: {cookies}")
except Exception as e:
    print(f"   Error: {e}")

# Step 4: Test refresh
print(f"\n4. Testing token refresh...")
try:
    refresh_response = session.post(
        f"{BACKEND_URL}/auth/refresh",
        timeout=5
    )
    print(f"   Status: {refresh_response.status_code}")
    if refresh_response.status_code == 200:
        refresh_data = refresh_response.json()
        new_token = refresh_data.get("access_token")
        print(f"   - New token: {new_token[:50]}...")
    else:
        print(f"   X Refresh failed: {refresh_response.text}")
except Exception as e:
    print(f"   X Error: {e}")

print("\n" + "=" * 70)
print("OK Backend auth flow test complete!")
print("=" * 70)
print("\nTroubleshooting:")
print("- If login role is not 'ADMIN', check DB role_id for user")
print("- If /me role is not 'ADMIN', check user.role relationship")
print("- If /me returns 401, token is invalid or expired")
print("- If refresh fails, check refresh_token cookie and backend logs")
print("=" * 70)
