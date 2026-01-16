from app.models import User
from app.models import db, User, initialize_db

print("1. Creating database tables...")
initialize_db()
print("2. Creating Admin user...")

try:
    User.create(
        name="Admin", 
        email="admin@example.com", 
        password="password123"
    )
    print("✅ SUCCESS: User 'admin@example.com' created")
except Exception as e:
    if "UNIQUE constraint failed" in str(e):
        print(" User already exists.")
    else:
        print(f"ERROR: {e}")