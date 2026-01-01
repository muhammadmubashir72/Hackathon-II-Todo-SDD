"""
Task validation skill for Todo CLI application
Validates all task operations before execution to ensure data integrity
"""

from typing import Optional, Dict, List, Any
from src.models.task import Task, TaskList


def validate_task_title(title: str) -> Dict[str, Any]:
    """
    Validate task title according to business rules.

    Args:
        title: Raw title string to validate

    Returns:
        Dictionary with:
            - valid (bool): True if validation passes
            - error (str): Error message if validation fails
            - normalized_title (str): Trimmed and normalized title
    """
    if not title or title.strip() == "":
        return {
            "valid": False,
            "error": "Title cannot be empty or contain only whitespace. Please provide a descriptive title.",
            "normalized_title": None
        }

    normalized = title.strip()
    if len(normalized) == 0:
        return {
            "valid": False,
            "error": "Title cannot be empty or contain only whitespace. Please provide a descriptive title.",
            "normalized_title": None
        }

    if len(normalized) > 200:
        return {
            "valid": False,
            "error": f"Title is too long ({len(normalized)} characters). Maximum 200 characters allowed.",
            "normalized_title": None
        }

    return {
        "valid": True,
        "error": None,
        "normalized_title": normalized
    }


def validate_task_id(task_id: int, task_list: TaskList) -> Dict[str, any]:
    """
    Validate task ID existence in the system.

    Args:
        task_id: Task ID to validate
        task_list: TaskList collection to check against

    Returns:
        Dictionary with:
            - valid (bool): True if validation passes
            - error (str): Error message if validation fails
            - task (Task): Task if found, None otherwise
    """
    task = task_list.get_by_id(task_id)

    if task is None:
        return {
            "valid": False,
            "error": f"Task #{task_id} does not exist. View all tasks to find correct ID.",
            "task": None
        }

    return {
        "valid": True,
        "error": None,
        "task": task
    }


def validate_task_update(task_id: int, title: Optional[str], task_list: TaskList) -> Dict[str, Any]:
    """
    Validate task update operation.

    Args:
        task_id: Task ID to update
        title: New title (optional)
        task_list: TaskList collection to check against

    Returns:
        Dictionary with:
            - valid (bool): True if validation passes
            - error (str): Error message if validation fails
            - task (Task): Task if found, None otherwise
            - normalized_title (str): Normalized title if provided
    """
    # Validate task ID exists
    id_result = validate_task_id(task_id, task_list)
    if not id_result["valid"]:
        return id_result

    # Validate title if provided
    if title is not None:
        title_result = validate_task_title(title)
        if not title_result["valid"]:
            return {
                "valid": False,
                "error": title_result["error"],
                "task": id_result["task"],
                "normalized_title": None
            }

        return {
            "valid": True,
            "error": None,
            "task": id_result["task"],
            "normalized_title": title_result["normalized_title"]
        }

    return {
        "valid": True,
        "error": None,
        "task": id_result["task"],
        "normalized_title": None
    }


def validate_duplicate_title(title: str, task_list: TaskList) -> Dict[str, Any]:
    """
    Check if task title already exists (duplicate prevention).

    Args:
        title: Title to check for duplicates
        task_list: TaskList collection to check against

    Returns:
        Dictionary with:
            - valid (bool): True if no duplicate
            - error (str): Error message if duplicate found
    """
    normalized = title.strip()
    for task in task_list.list_all():
        if task.title == normalized:
            return {
                "valid": False,
                "error": f"A task with this title already exists:\n• Task #{task.id}: {task.title} ({task.status})\n\nWhat you can do:\n• Update the existing task: [US3] Update task\n• Use a different title"
            }

    return {
        "valid": True,
        "error": None
    }
