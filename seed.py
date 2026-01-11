from app.models import User
from app.models import db
db.connect()
try:
    User.create(name="Admin", email="admin@example.com", password="password123")
    print("User 'admin@example.com' created successfully!")
except Exception as e:
    print(f"User already exist: {e}")
db.close()