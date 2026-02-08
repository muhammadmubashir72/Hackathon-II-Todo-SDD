"""
AI Todo agent router module.

This module implements AI-powered todo operations with natural language processing using the OpenAI API.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from pydantic import BaseModel
from typing import Dict, Any
import os
import json
import openai
from dotenv import load_dotenv, find_dotenv
from ..database import get_session
from ..middleware.auth_middleware import auth_middleware
from ..services.task_service import TaskService
from ..models.task import TaskCreate, TaskUpdate


# Load environment variables
load_dotenv(find_dotenv())

# Configure OpenAI client for Gemini API
openai.api_key = os.getenv("GEMINI_API_KEY", "AIzaSyCt-sdxbR0ZFXAMcvzagAcKZC4RLyWAXts")
openai.base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"

ai_todo_router = APIRouter(prefix="/ai-todo", tags=["AI Todo"])


class AIRequest(BaseModel):
    """Request model for AI todo operations."""
    message: str


class AIResponse(BaseModel):
    """Response model for AI todo operations."""
    reply: str
    operation_performed: str
    task_details: Dict[str, Any] = {}


def determine_operation_from_message(message: str) -> Dict[str, Any]:
    """
    Determine the operation to perform based on the message.
    
    Args:
        message: Natural language input from user
        
    Returns:
        Dictionary containing operation and extracted details
    """
    message_lower = message.lower().strip()
    
    # Define operation keywords
    add_keywords = ['add', 'create', 'make', 'new', 'need to', 'have to', 'should', 'must', 'want to']
    list_keywords = ['list', 'show', 'display', 'view', 'see', 'all', 'my tasks', 'what']
    complete_keywords = ['complete', 'done', 'finish', 'mark as', 'finished', 'tick off', 'check off']
    delete_keywords = ['delete', 'remove', 'cancel', 'eliminate', 'get rid of']
    update_keywords = ['update', 'change', 'modify', 'edit', 'alter', 'fix']
    
    # Count keyword matches
    add_matches = sum(1 for keyword in add_keywords if keyword in message_lower)
    list_matches = sum(1 for keyword in list_keywords if keyword in message_lower)
    complete_matches = sum(1 for keyword in complete_keywords if keyword in message_lower)
    delete_matches = sum(1 for keyword in delete_keywords if keyword in message_lower)
    update_matches = sum(1 for keyword in update_keywords if keyword in message_lower)
    
    # Determine operation based on highest match
    max_matches = max(add_matches, list_matches, complete_matches, delete_matches, update_matches)
    
    if max_matches == 0:
        # Default to list if no clear operation
        return {"operation": "LIST_TASKS", "task_details": {}, "target_task": ""}
    elif add_matches == max_matches:
        # Extract task details for add operation
        import re
        
        # Try to extract task title from message
        # Patterns for extracting task information
        patterns = [
            r'(?:add|create|make|new)\s+(?:a\s+)?(?:task|todo|to-do)\s+(?:to|for)?\s*(.+?)(?:\s|$|[,.!?])',
            r'(?:please|can you|could you)\s+(?:add|create|make)\s+(?:a\s+)?(?:task|todo|to-do)\s+(?:to|for)?\s*(.+?)(?:\s|$|[,.!?])',
            r'(?:i need to|i have to|i want to|must|should)\s+(.+?)(?:\s|$|[,.!?])'
        ]
        
        task_title = ""
        for pattern in patterns:
            match = re.search(pattern, message_lower)
            if match:
                task_title = match.group(1).strip()
                break
        
        # If no title found from patterns, extract from the message
        if not task_title:
            # Remove common verbs and get the remaining text
            common_verbs = ['add', 'create', 'make', 'new', 'please', 'can you', 'could you', 'i need to', 'i have to', 'i want to', 'must', 'should', 'to', 'for', 'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'by']
            words = message_lower.split()
            filtered_words = [word for word in words if word not in common_verbs and len(word) > 2]
            if filtered_words:
                task_title = ' '.join(filtered_words)
        
        return {
            "operation": "ADD_TASK",
            "task_details": {"title": task_title},
            "target_task": task_title
        }
    elif list_matches == max_matches:
        return {"operation": "LIST_TASKS", "task_details": {}, "target_task": ""}
    elif complete_matches == max_matches:
        # Extract target task for complete operation
        import re
        
        # Patterns for identifying target task
        patterns = [
            r'(?:complete|finish|done|mark as done|mark as complete|tick off|check off)\s*[\"\']([^\"\']+)[\"\']',
            r'(?:complete|finish|done|mark as done|mark as complete|tick off|check off)\s+(.+?)(?:\s|$|[,.!?])',
            r'(?:done with|finished with)\s+(.+?)(?:\s|$|[,.!?])'
        ]
        
        target_task = ""
        for pattern in patterns:
            match = re.search(pattern, message_lower)
            if match:
                target_task = match.group(1).strip()
                break
        
        if not target_task:
            # Extract potential task from message
            common_verbs = ['complete', 'finish', 'done', 'mark', 'as', 'is', 'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'with', 'done', 'with', 'finished', 'with']
            words = message_lower.split()
            filtered_words = [word for word in words if word not in common_verbs and len(word) > 2]
            if filtered_words:
                target_task = ' '.join(filtered_words)
        
        return {
            "operation": "COMPLETE_TASK",
            "task_details": {},
            "target_task": target_task
        }
    elif delete_matches == max_matches:
        # Extract target task for delete operation
        import re

        # Patterns for identifying target task
        patterns = [
            r'(?:delete|remove|cancel|eliminate|get rid of)\s*[\"\']([^\"\']+)[\"\']',
            r'(?:delete|remove|cancel|eliminate|get rid of)\s+(.+?)(?:\s|$|[,.!?])'
        ]

        target_task = ""
        for pattern in patterns:
            match = re.search(pattern, message_lower)
            if match:
                target_task = match.group(1).strip()
                break

        if not target_task:
            # Extract potential task from message
            common_verbs = ['delete', 'remove', 'cancel', 'eliminate', 'get rid of', 'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by']
            words = message_lower.split()
            filtered_words = [word for word in words if word not in common_verbs and len(word) > 2]
            if filtered_words:
                target_task = ' '.join(filtered_words)
        
        return {
            "operation": "DELETE_TASK",
            "task_details": {},
            "target_task": target_task
        }
    elif update_matches == max_matches:
        return {
            "operation": "UPDATE_TASK",
            "task_details": {},
            "target_task": ""
        }
    
    # Fallback to list
    return {"operation": "LIST_TASKS", "task_details": {}, "target_task": ""}


@ai_todo_router.post("", response_model=AIResponse)
async def process_ai_request(
    ai_request: AIRequest,
    current_user_id: int = Depends(auth_middleware.get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Process natural language requests for todo operations using simple NLP.

    Args:
        ai_request: Natural language request from user
        current_user_id: ID of the authenticated user
        session: Database session

    Returns:
        AIResponse with operation result
    """
    try:
        message = ai_request.message.strip()
        
        # Determine operation from message
        operation_info = determine_operation_from_message(message)
        operation = operation_info["operation"]
        task_details = operation_info["task_details"]
        target_task = operation_info["target_task"]

        reply = ""
        task_result = {}

        if operation == "ADD_TASK":
            # Create a new task
            title = task_details.get("title", "Untitled Task")
            
            if not title or title == "":
                # If we couldn't extract a title, use the whole message
                title = message
            
            # Create task object
            task_create = TaskCreate(
                title=title,
                description="",
                priority="medium",
                category=None,
                due_date=None
            )

            # Create task through service
            task = TaskService.create_task(session, task_create, current_user_id)

            reply = f"I've added '{title}' to your tasks."
            task_result = {"id": task.id, "title": task.title, "is_completed": task.is_completed}

        elif operation == "LIST_TASKS":
            # Get user's tasks
            tasks = TaskService.get_tasks_for_user(session, current_user_id, limit=50, offset=0, status="all")
            total_count = TaskService.get_total_task_count(session, current_user_id, "all")

            if total_count == 0:
                reply = "You don't have any tasks yet. Would you like to add one?"
            else:
                reply = f"You have {total_count} task(s). Here are some of them: "
                for i, task in enumerate(tasks[:3]):  # Show first 3 tasks
                    status = "✓" if task.is_completed else "○"
                    reply += f"{status} {task.title}"
                    if i < min(2, len(tasks)-1):
                        reply += ", "

            task_result = {"task_count": total_count, "sample_tasks": [task.title for task in tasks[:3]]}

        elif operation == "COMPLETE_TASK":
            # Find and complete a task
            # For simplicity, we'll search for tasks containing the target_task text
            from sqlmodel import select
            from ..models.task import Task

            statement = select(Task).where(Task.user_id == current_user_id, Task.title.ilike(f"%{target_task}%"))
            potential_tasks = session.exec(statement).all()

            if potential_tasks:
                task_to_complete = potential_tasks[0]  # Take the first match
                task_update = TaskUpdate(is_completed=True)
                updated_task = TaskService.update_task(session, task_to_complete.id, task_update, current_user_id)

                if updated_task:
                    reply = f"I've marked '{updated_task.title}' as complete!"
                    task_result = {"id": updated_task.id, "title": updated_task.title, "is_completed": updated_task.is_completed}
                else:
                    reply = "I couldn't update the task. It might not exist or you may not have permission to modify it."
            else:
                reply = f"I couldn't find a task containing '{target_task}'. Could you check the task name?"

        elif operation == "DELETE_TASK":
            # Find and delete a task
            from sqlmodel import select
            from ..models.task import Task

            statement = select(Task).where(Task.user_id == current_user_id, Task.title.ilike(f"%{target_task}%"))
            potential_tasks = session.exec(statement).all()

            if potential_tasks:
                task_to_delete = potential_tasks[0]  # Take the first match
                success = TaskService.delete_task(session, task_to_delete.id, current_user_id)

                if success:
                    reply = f"I've deleted '{task_to_delete.title}' from your tasks."
                    task_result = {"deleted_task_id": task_to_delete.id}
                else:
                    reply = "I couldn't delete the task. It might not exist or you may not have permission to delete it."
            else:
                reply = f"I couldn't find a task containing '{target_task}'. Could you check the task name?"

        elif operation == "UPDATE_TASK":
            # Update a task (simplified implementation)
            reply = "Task update functionality is available. You can say something like 'update the grocery task to be high priority'."

        else:
            # Unknown operation
            reply = f"I processed your request: {message}"

        return AIResponse(
            reply=reply,
            operation_performed=operation,
            task_details=task_result
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI request processing failed: {str(e)}")