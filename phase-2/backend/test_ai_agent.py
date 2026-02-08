"""
Test script for AI Todo Agent functionality.

This script tests the natural language processing capabilities of the AI agent.
"""

import asyncio
import sys
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.agents.todo_agent import run_todo_agent


async def test_ai_agent():
    """Test the AI agent with various natural language inputs."""
    
    # Mock user ID for testing
    user_id = 1
    
    test_cases = [
        "Add a task to buy groceries",
        "Create a task to call mom tomorrow",
        "Show me my tasks",
        "Mark the groceries task as complete",
        "Delete the groceries task",
        "Add a high priority task to finish the report",
        "List my completed tasks",
        "I need to schedule a meeting with John next week"
    ]
    
    print("Testing AI Todo Agent...\n")
    
    for i, message in enumerate(test_cases, 1):
        print(f"Test {i}: '{message}'")
        try:
            result = await run_todo_agent(user_id, message)
            print(f"  Reply: {result.get('reply', 'No reply')}")
            print(f"  Operation: {result.get('operation_performed', 'None')}")
            print(f"  Success: {result.get('success', False)}")
            print()
        except Exception as e:
            print(f"  Error: {str(e)}")
            print()
    
    print("AI agent testing completed.")


if __name__ == "__main__":
    asyncio.run(test_ai_agent())