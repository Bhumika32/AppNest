#!/usr/bin/env python3
"""
Test script to verify admin authorization is working after JWT role normalization fix.
Run this after starting the backend server.
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"
ADMIN_EMAIL = "bg226104@gmail.com"
ADMIN_PASSWORD = "Password@123"  # You may need to update this

def print_section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def test_admin_flow():
    """Test the complete admin authentication and access flow."""
    
    print_section("STEP 1: TEST ADMIN LOGIN")
    
    login_data = {
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"❌ Login failed: {response.text}")
        return False
    
    login_response = response.json()
    print(f"✅ Login successful!")
    print(f"   User: {login_response['user']['email']}")
    print(f"   Role: {login_response['user']['role']}")
    
    access_token = login_response.get('access_token')
    if not access_token:
        print("❌ No access token received!")
        return False
    
    print(f"   Access Token: {access_token[:50]}...")
    
    # Extract and decode the JWT to verify role is lowercase
    print("\n   📋 Analyzing JWT claims...")
    try:
        import jwt
        decoded = jwt.decode(access_token, options={"verify_signature": False})
        jwt_role = decoded.get('role')
        print(f"   JWT Role Claim: '{jwt_role}' (type: {type(jwt_role).__name__})")
        if jwt_role == 'admin':
            print(f"   ✅ JWT role is lowercase 'admin' - CORRECT!")
        else:
            print(f"   ⚠️  JWT role is '{jwt_role}' - should be lowercase 'admin'")
    except Exception as e:
        print(f"   ⚠️  Could not decode JWT: {e}")
    
    # Now test admin endpoints
    headers = {"Authorization": f"Bearer {access_token}"}
    
    print_section("STEP 2: TEST ADMIN ANALYTICS ENDPOINTS")
    
    endpoints = [
        "/admin/analytics/overview",
        "/admin/analytics/users",
        "/admin/analytics/games",
        "/admin/analytics/tools"
    ]
    
    all_passed = True
    for endpoint in endpoints:
        response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
        status = "✅" if response.status_code == 200 else "❌"
        print(f"{status} GET {endpoint}: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   Response: {response.text[:200]}")
            all_passed = False
    
    return all_passed

if __name__ == "__main__":
    print("🔐 Admin Authorization Test")
    print("=" * 60)
    
    try:
        success = test_admin_flow()
        
        print_section("FINAL RESULT")
        if success:
            print("✅ ALL TESTS PASSED! Admin authorization is working correctly.")
        else:
            print("❌ Some tests failed. Check the output above for details.")
            print("\nNext steps:")
            print("1. Verify admin user email and password are correct")
            print("2. Check backend logs for 403 errors")
            print("3. Ensure user role_id points to admin role in database")
    
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to backend at http://localhost:5000")
        print("   Make sure the backend server is running: python run.py")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
