"""
Task state management skill module.

This module governs task lifecycle and state transitions following the reusable skills architecture.
"""

from datetime import datetime
from typing import Optional
from sqlmodel import Session
from ..models.task import Task


def transition_task_to_completed(task: Task) -> Task:
    """
    Transition a task from pending to completed state.

    Args:
        task: Task object to transition

    Returns:
        Updated task object with completed state
    """
    task.is_completed = True
    task.completed_at = datetime.utcnow()
    task.updated_at = datetime.utcnow()

    return task


def transition_task_to_pending(task: Task) -> Task:
    """
    Transition a task from completed to pending state.

    Args:
        task: Task object to transition

    Returns:
        Updated task object with pending state
    """
    task.is_completed = False
    task.completed_at = None
    task.updated_at = datetime.utcnow()

    return task


def validate_state_transition(current_state: bool, target_state: bool) -> tuple[bool, Optional[str]]:
    """
    Validate if a state transition is allowed.

    Args:
        current_state: Current completion status of the task
        target_state: Target completion status for the transition

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Prevent redundant state transitions (trying to set a task to a state it's already in)
    if current_state == target_state:
        if current_state:
            return False, "Task is already completed"
        else:
            return False, "Task is already pending"

    return True, None


def update_task_completion_status(
    session: Session,
    task_id: int,
    target_status: bool
) -> Task:
    """
    Update task completion status with proper state management.

    Args:
        session: Database session
        task_id: ID of the task to update
        target_status: Target completion status (True for completed, False for pending)

    Returns:
        Updated task object

    Raises:
        ValueError if transition is invalid
    """
    task = session.get(Task, task_id)
    if not task:
        raise ValueError(f"Task with ID {task_id} not found")

    # Only validate the state transition if the status is actually changing
    if task.is_completed != target_status:
        # Validate the state transition
        is_valid, error_msg = validate_state_transition(task.is_completed, target_status)
        if not is_valid:
            raise ValueError(error_msg)

    # Apply the appropriate transition only if the status is actually changing
    if task.is_completed != target_status:
        if target_status:
            return transition_task_to_completed(task)
        else:
            return transition_task_to_pending(task)
    else:
        # If status is not changing, just return the existing task with updated timestamp
        task.updated_at = datetime.utcnow()
        return task


def is_task_completed(task: Task) -> bool:
    """
    Check if a task is completed.

    Args:
        task: Task object to check

    Returns:
        Boolean indicating completion status
    """
    return task.is_completed


def is_task_pending(task: Task) -> bool:
    """
    Check if a task is pending.

    Args:
        task: Task object to check

    Returns:
        Boolean indicating if task is pending
    """
    return not task.is_completed


def validate_task_lifecycle_operations(task: Task) -> tuple[bool, Optional[str]]:
    """
    Validate that a task is in a valid state for lifecycle operations.

    Args:
        task: Task object to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if task is None:
        return False, "Task cannot be None"

    # Additional validation can be added here as needed
    return True, None


def prepare_task_for_modification(task: Task) -> Task:
    """
    Prepare a task for modification by updating its timestamp.

    Args:
        task: Task object to prepare

    Returns:
        Task object with updated timestamp
    """
    task.updated_at = datetime.utcnow()
    return task


def archive_task_if_needed(task: Task, days_since_completion: int = 30) -> Task:
    """
    Archive a task if it has been completed for a specified number of days.

    Args:
        task: Task object to check for archiving
        days_since_completion: Number of days after which to archive completed tasks

    Returns:
        Updated task object
    """
    if task.is_completed and task.completed_at:
        days_passed = (datetime.utcnow() - task.completed_at).days
        if days_passed >= days_since_completion:
            # In a real implementation, you might set an 'archived' flag
            # For now, we'll just update the timestamp
            task.updated_at = datetime.utcnow()

    return task