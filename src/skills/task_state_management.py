"""
Task state management skill for Todo CLI application
Governs task lifecycle and state transitions
"""

from typing import Dict, Any
from src.lib.utils import get_current_timestamp
from src.models.task import Task


def transition_state(task: Task, new_state: str) -> Dict[str, Any]:
    """
    Perform valid state transition (Pending ↔ Completed).

    Args:
        task: Task object to transition
        new_state: Target state ("Pending" or "Completed")

    Returns:
        Dictionary with:
            - valid (bool): True if transition succeeds
            - error (str): Error message if transition fails
            - task (Task): Task with updated status
    """
    # Validate states
    if new_state not in ["Pending", "Completed"]:
        return {
            "valid": False,
            "error": f"Invalid state: {new_state}. Must be 'Pending' or 'Completed'.",
            "task": task
        }

    # Check current state
    current_state = task.status

    # Valid transitions
    if current_state == "Pending" and new_state == "Completed":
        task.status = new_state
        task.updated_at = get_current_timestamp()
        return {
            "valid": True,
            "error": None,
            "task": task
        }

    if current_state == "Completed" and new_state == "Pending":
        task.status = new_state
        task.updated_at = get_current_timestamp()
        return {
            "valid": True,
            "error": None,
            "task": task
        }

    # Invalid transitions (no state change)
    if current_state == new_state:
        if current_state == "Pending":
            return {
                "valid": False,
                "error": f"Task #{task.id} is already pending. No change needed.",
                "task": task
            }
        else:  # Already completed
            return {
                "valid": False,
                "error": f"Task #{task.id} is already completed. No change needed.",
                "task": task
            }

    # Any other transition is invalid
    return {
        "valid": False,
        "error": f"Invalid transition: {current_state} → {new_state}",
        "task": task
    }


def can_transition_to_completed(task: Task) -> bool:
    """
    Check if task can transition to Completed state.

    Args:
        task: Task to check

    Returns:
        bool: True if transition is valid
    """
    return task.status == "Pending"


def can_transition_to_pending(task: Task) -> bool:
    """
    Check if task can transition to Pending state.

    Args:
        task: Task to check

    Returns:
        bool: True if transition is valid
    """
    return task.status == "Completed"


def get_state_description(state: str) -> str:
    """
    Get human-readable description of task state.

    Args:
        state: Task state string

    Returns:
        Human-readable description
    """
    state_map = {
        "Pending": "Pending - Task not yet completed",
        "Completed": "Completed - Task finished successfully"
    }
    return state_map.get(state, state)


def validate_state_transition(task_id: int, current_state: str, target_state: str, timestamp: str = None) -> Dict[str, any]:
    """
    Validate if state transition is allowed before applying.

    Args:
        task_id: Task ID
        current_state: Current task status
        target_state: Desired state
        timestamp: Optional timestamp of when current state was set

    Returns:
        Dictionary with:
            - valid (bool): True if transition is valid
            - error (str): Error message if invalid
            - suggestion (str): Alternative action suggestion
    """
    # Check for no state change
    if current_state == target_state:
        if current_state == "Pending":
            return {
                "valid": False,
                "error": f"Task #{task_id} is already pending. No change needed.",
                "suggestion": "Mark as complete"
            }
        else:  # Already completed
            error_msg = f"Task #{task_id} is already completed"
            if timestamp:
                error_msg += f" (completed at {timestamp})"
            return {
                "valid": False,
                "error": error_msg,
                "suggestion": "Mark as incomplete"
            }

    # Only two valid transitions allowed
    valid_transitions = [
        ("Pending", "Completed"),
        ("Completed", "Pending")
    ]

    transition = (current_state, target_state)
    if transition not in valid_transitions:
        return {
            "valid": False,
            "error": f"Invalid transition: {current_state} → {target_state}",
            "suggestion": "View task details first"
        }

    return {
        "valid": True,
        "error": None,
        "suggestion": None
    }
