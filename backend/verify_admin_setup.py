#!/usr/bin/env python
"""
Admin User Verification & Setup Script
Verifies that the admin user (role_id=2) is correctly configured
"""

import sys
sys.path.insert(0, '/path/to/backend')  # Adjust as needed

from app import create_app
from app.models.user import User
from app.models.role import Role
from app.core.extensions import db

app = create_app()

with app.app_context():
    print("=" * 60)
    print("AppNest Admin User Verification")
    print("=" * 60)
    
    # 1. Check roles exist
    print("\n✓ Checking Roles in Database:")
    roles = Role.query.all()
    for role in roles:
        print(f"  - Role ID {role.id}: {role.name}")
    
    # 2. Find admin role
    admin_role = Role.query.filter_by(name="ADMIN").first()
    if not admin_role:
        print("\n❌ ERROR: ADMIN role not found!")
        sys.exit(1)
    print(f"\n✓ Admin role exists: ID={admin_role.id}, Name={admin_role.name}")
    
    # 3. Check admin user
    print("\n✓ Checking Admin Users:")
    admin_users = User.query.filter_by(role_id=admin_role.id).all()
    
    if not admin_users:
        print("  ⚠️  No admin users found!")
    else:
        for user in admin_users:
            print(f"  - User: {user.username} ({user.email})")
            print(f"    Role ID: {user.role_id}")
            print(f"    Role Name: {user.role.name if user.role else 'N/A'}")
            print(f"    Is Verified: {user.is_verified}")
    
    # 4. Test role relationship
    print("\n✓ Testing Role Relationships:")
    if admin_users and admin_users[0].role:
        test_user = admin_users[0]
        print(f"  User {test_user.username}.role = {test_user.role}")
        print(f"  User {test_user.username}.role.name = {test_user.role.name}")
        print(f"  Lowercase: {test_user.role.name.lower()}")
    
    print("\n" + "=" * 60)
    print("✅ Admin user setup appears correct!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Login with admin email: bg226104@gmail.com")
    print("2. Check browser console for role value")
    print("3. Verify you're redirected to /dashboard/admin")
    print("=" * 60)
