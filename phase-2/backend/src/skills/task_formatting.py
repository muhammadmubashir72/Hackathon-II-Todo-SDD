"""
Task formatting skill module.

This module handles formatting of task data for API responses following the reusable skills architecture.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from ..models.task import Task


def format_task_response(task: Task) -> Dict[str, Any]:
    """
    Format a task for API response.

    Args:
        task: Task object to format

    Returns:
        Dictionary representing the formatted task
    """
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "is_completed": task.is_completed,
        "created_at": task.created_at.isoformat() if task.created_at else None,
        "completed_at": task.completed_at.isoformat() if task.completed_at else None,
        "updated_at": task.updated_at.isoformat() if task.updated_at else None,
        "user_id": task.user_id,
        # New fields
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "status": task.status.value if hasattr(task.status, 'value') else task.status,
        "priority": task.priority.value if hasattr(task.priority, 'value') else task.priority,
        "category": task.category,
        "tags": task.tags
    }


def format_tasks_list_response(tasks: List[Task], total_count: int, limit: int, offset: int) -> Dict[str, Any]:
    """
    Format a list of tasks for API response with pagination.

    Args:
        tasks: List of task objects to format
        total_count: Total number of tasks available
        limit: Number of tasks requested
        offset: Offset for pagination

    Returns:
        Dictionary representing the formatted response
    """
    formatted_tasks = [format_task_response(task) for task in tasks]

    return {
        "tasks": formatted_tasks,
        "pagination": {
            "total": total_count,
            "limit": limit,
            "offset": offset
        }
    }


def format_user_response(user) -> Dict[str, Any]:
    """
    Format a user for API response.

    Args:
        user: User object to format

    Returns:
        Dictionary representing the formatted user
    """
    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None,
        "is_active": user.is_active
    }


def format_success_response(message: str) -> Dict[str, str]:
    """
    Format a generic success response.

    Args:
        message: Success message

    Returns:
        Dictionary representing the success response
    """
    return {
        "message": message
    }


def format_token_response(access_token: str, token_type: str = "bearer", user=None, refresh_token: str = None) -> Dict[str, Any]:
    """
    Format a token response for authentication endpoints.

    Args:
        access_token: JWT access token
        token_type: Token type (default: "bearer")
        user: Optional user object to include in response
        refresh_token: Optional refresh token

    Returns:
        Dictionary representing the token response
    """
    response = {
        "access_token": access_token,
        "token": access_token,  # For compatibility with frontend
        "token_type": token_type
    }

    if refresh_token:
        response["refresh_token"] = refresh_token

    if user:
        response["user"] = format_user_response(user)

    return response


def format_datetime(dt: Optional[datetime]) -> Optional[str]:
    """
    Format a datetime object as ISO string.

    Args:
        dt: Datetime object to format

    Returns:
        ISO formatted datetime string or None
    """
    if dt is None:
        return None
    return dt.isoformat()


def format_boolean(value: Any) -> bool:
    """
    Format a value as boolean.

    Args:
        value: Value to convert to boolean

    Returns:
        Boolean representation of the value
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ('true', '1', 'yes', 'on')
    if isinstance(value, int):
        return bool(value)
    return bool(value)