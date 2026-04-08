import os
from app import create_app
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.role import Role

app = create_app()
with app.app_context(db=Session) as db:
    admin_role = Role.query.filter_by(name='ADMIN').first()
    if not admin_role:
        admin_role = Role(name='ADMIN')
        db.add(admin_role)
        db.commit()
        print("Created ADMIN role.")

    admin_user = User.query.filter_by(email='admin@appnest.com').first()
    if not admin_user:
        admin_user = User(
            username='admin',
            email='admin@appnest.com',
            role_id=admin_role.id,
            is_verified=True
        )
        admin_user.set_password('password123')
        db.add(admin_user)
        db.commit()
        print("Created Admin User: admin@appnest.com : password123")
    else:
        # Just reset the password so we know for sure what it is
        admin_user.set_password('password123')
        admin_user.is_verified = True
        admin_user.role_id = admin_role.id
        db.commit()
        print("Admin user already existed, reset password to: password123")
