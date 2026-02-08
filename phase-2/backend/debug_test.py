#!/usr/bin/env python3
"""
Debug script to test individual components of the task creation process.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from src.skills.input_parsing import parse_task_input
from src.models.task import TaskCreate
from datetime import datetime

def test_input_parsing():
    print("Testing input parsing...")
    
    # Test data similar to what the frontend sends
    raw_data = {
        "title": "Test Task",
        "description": "Test Description",
        "tags": None
    }
    
    try:
        parsed_data = parse_task_input(raw_data)
        print(f"Parsed data: {parsed_data}")
        
        # Try to create TaskCreate model
        task_create = TaskCreate(**parsed_data)
        print(f"TaskCreate model created successfully: {task_create}")
        
        # Test with model_dump() method
        dumped_data = task_create.model_dump()
        print(f"Model dump: {dumped_data}")
        
        print("Input parsing test PASSED")
    except Exception as e:
        print(f"Input parsing test FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_input_parsing()