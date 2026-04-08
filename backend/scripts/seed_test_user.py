import sys
import os

# Add the project root to sys.path
sys.path.append(os.getcwd())
from app.core.database import SessionLocal
from app.models.user import User
from app.models.role import Role

def seed_test_user():
    session = SessionLocal()
    try:
        # 1. Ensure Roles exist
        admin_role = session.query(Role).filter_by(name="ADMIN").first()
        if not admin_role:
            admin_role = Role(name="ADMIN")
            session.add(admin_role)
            session.commit()
            print("Created ADMIN role.")
        
        user_role = session.query(Role).filter_by(name="USER").first()
        if not user_role:
            user_role = Role(name="USER")
            session.add(user_role)
            session.commit()
            print("Created USER role.")

        # 2. Seed the specific user for tests/test_auth_backend.py
        test_email = "bg226104@gmail.com"
        test_user = session.query(User).filter_by(email=test_email).first()
        
        if not test_user:
            test_user = User(
                username="test_admin",
                email=test_email,
                role_id=admin_role.id,
                is_verified=True
            )
            test_user.set_password("password")
            session.add(test_user)
            session.commit()
            print(f"Created Test Admin: {test_email} : password")
        else:
            test_user.role_id = admin_role.id
            test_user.is_verified = True
            test_user.set_password("password")
            session.commit()
            print(f"Updated existing Test Admin: {test_email} : password")

    except Exception as e:
        print(f"Error seeding user: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    seed_test_user()
