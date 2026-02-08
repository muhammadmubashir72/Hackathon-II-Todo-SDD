#!/usr/bin/env python3
"""
Full debug script to test the entire task creation process.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from src.skills.input_parsing import parse_task_input
from src.models.task import TaskCreate
from src.database import get_session, create_tables
from src.services.task_service import TaskService
from datetime import datetime

def test_full_process():
    print("Testing full task creation process...")
    
    # Create tables first
    create_tables()
    print("Tables created")
    
    # Test data similar to what the frontend sends
    raw_data = {
        "title": "Test Task",
        "description": "Test Description",
        "tags": None
    }
    
    try:
        print("Step 1: Parsing input...")
        parsed_data = parse_task_input(raw_data)
        print(f"Parsed data: {parsed_data}")
        
        print("Step 2: Creating TaskCreate model...")
        task_create = TaskCreate(**parsed_data)
        print(f"TaskCreate model: {task_create}")
        
        print("Step 3: Getting database session...")
        session_gen = get_session()
        session = next(session_gen)
        print("Database session acquired")
        
        # Create a test user first (since tasks require a user)
        from src.models.user import User
        from sqlmodel import select
        
        # Check if test user exists, if not create one
        existing_users = session.exec(select(User)).all()
        if not existing_users:
            test_user = User(
                email="test@example.com",
                hashed_password="hashed_test_password",
                is_active=True
            )
            session.add(test_user)
            session.commit()
            session.refresh(test_user)
            user_id = test_user.id
            print(f"Created test user with ID: {user_id}")
        else:
            user_id = existing_users[0].id
            print(f"Using existing user with ID: {user_id}")
        
        print(f"Step 4: Creating task for user ID: {user_id}")
        task = TaskService.create_task(session, task_create, user_id)
        print(f"Task created successfully: {task}")
        
        session.close()
        print("Full process test PASSED")
        
    except Exception as e:
        print(f"Full process test FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_full_process()