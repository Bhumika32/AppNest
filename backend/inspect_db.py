from app import create_app
from app.models.user import User

app = create_app()

with app.app_context():
    users = User.query.all()
    print("-" * 50)
    print(f"Total Users: {len(users)}")
    print("-" * 50)
    for u in users:
        print(f"ID: {u.id} | Email: {u.email} | Verified: {u.is_verified}")
    print("-" * 50)
