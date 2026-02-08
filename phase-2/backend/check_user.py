#!/usr/bin/env python3
"""
Script to check if a user exists in the database and create one if needed.
"""

import os
from sqlmodel import SQLModel, Session, select
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import models and database
from src.models.user import User
from src.database import engine, create_tables
from src.services.user_service import UserService
from src.skills.auth_validation import validate_password_strength


def check_or_create_user():
    """Check if user exists, and create if not."""
    
    # Create tables if they don't exist
    create_tables()
    
    # Create a session
    with Session(engine) as session:
        # Check if user exists
        email = "mubashirkhi72@gmail.com"
        user = session.exec(select(User).where(User.email == email)).first()
        
        if user:
            print(f"User with email '{email}' exists!")
            print(f"User ID: {user.id}")
            print(f"Active: {user.is_active}")
            print(f"Created: {user.created_at}")
        else:
            print(f"User with email '{email}' does not exist.")

            # Automatically create the user
            create_new = 'y'

            if create_new.lower() == 'y':
                password = "Mubashir@123"  # Using the password from your curl command
                
                # Validate password strength
                is_valid, error_msg = validate_password_strength(password)
                if not is_valid:
                    print(f"Password validation failed: {error_msg}")
                    return
                
                try:
                    # Create the user
                    user_create_data = {"email": email, "password": password}
                    from src.models.user import UserCreate
                    user_create = UserCreate(**user_create_data)
                    
                    user = UserService.create_user(session, user_create)
                    print(f"User created successfully!")
                    print(f"User ID: {user.id}")
                    print(f"Email: {user.email}")
                    print(f"Active: {user.is_active}")
                except Exception as e:
                    print(f"Error creating user: {e}")


if __name__ == "__main__":
    check_or_create_user()