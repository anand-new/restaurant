# create_initial_user.py

import uuid
from app.db.engine import SessionLocal
from app.models.user import User
from passlib.hash import pbkdf2_sha256 as hash

# Create DB session
db = SessionLocal()

# Define user credentials
username = "admin"
email = "admin@example.com"
password = "admin123"

# Hash password using pbkdf2_sha256
password_hash = hash.hash(password)

# Optional: set default role_id and created_by
default_role_id = 1  # You can adjust based on your roles table
created_by = None     # Since this is the first user

# Check if user already exists
existing_user = db.query(User).filter(User.email == email).first()
if existing_user:
    print("User already exists: %s", email)
else:
    # Create user object
    user = User(
        id=uuid.uuid4(),
        username=username,
        email=email,
        password_hash=password_hash,
        role_id=default_role_id,
        created_by=created_by
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print(" Created initial user: %s with password: %s",email,password)
