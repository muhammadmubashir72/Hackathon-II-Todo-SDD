"""
Task validation skill module.

This module contains validation logic for tasks following the reusable skills architecture.
"""

from typing import Optional
from sqlmodel import Session
from ..models.task import Task
from ..models.user import User


def validate_task_title(title: str) -> tuple[bool, Optional[str]]:
    """
    Validate task title according to business rules.

    Args:
        title: The task title to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not title or not title.strip():
        return False, "Task title cannot be empty or whitespace-only"

    if len(title.strip()) > 200:
        return False, "Task title must be 200 characters or less"

    return True, None


def validate_task_description(description: Optional[str]) -> tuple[bool, Optional[str]]:
    """
    Validate task description according to business rules.

    Args:
        description: The task description to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if description is not None and len(description) > 1000:
        return False, "Task description must be 1000 characters or less"

    return True, None


def validate_user_ownership(
    session: Session,
    task_id: int,
    user_id: int
) -> tuple[bool, Optional[str]]:
    """
    Validate that the given user owns the specified task.

    Args:
        session: Database session
        task_id: ID of the task to check
        user_id: ID of the user making the request

    Returns:
        Tuple of (is_valid, error_message)
    """
    task = session.get(Task, task_id)
    if not task:
        return False, "Task not found"

    if task.user_id != user_id:
        return False, "Task belongs to another user"

    return True, None


def validate_duplicate_task(
    session: Session,
    title: str,
    user_id: int
) -> tuple[bool, Optional[str]]:
    """
    Validate that a task with the same title doesn't already exist for the user.

    Args:
        session: Database session
        title: Title of the task to check
        user_id: ID of the user

    Returns:
        Tuple of (is_valid, error_message)
    """
    from sqlmodel import select
    
    statement = select(Task).where(Task.title == title, Task.user_id == user_id)
    existing_task = session.exec(statement).first()

    if existing_task:
        return False, "Task with this title already exists for this user"

    return True, None