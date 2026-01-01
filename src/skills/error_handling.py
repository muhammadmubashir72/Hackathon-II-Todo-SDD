"""
Error handling skill for Todo CLI application
Standardizes how errors are generated and displayed
"""

from typing import Optional, Dict, Any, List


def format_error(error_type: str, message: str, suggestions: List[str] = None) -> str:
    """
    Format error message with standard structure.

    Args:
        error_type: Error category (e.g., "Task Not Found", "Invalid Input")
        message: Error message
        suggestions: Optional list of suggestions

    Returns:
        Formatted error string
    """
    separator = "━" * 60
    header = f"\n{separator}\n❌ Error Type: {error_type}\n{separator}\n"
    content = f"{message}\n\n"

    if suggestions:
        suggestion_text = "What you can do:\n"
        for i, suggestion in enumerate(suggestions, 1):
            suggestion_text += f"• {suggestion}\n"
        content += suggestion_text

    footer = f"{separator}\n"

    return header + content + footer


def error_task_not_found(task_id: int) -> str:
    """
    Format task not found error.

    Args:
        task_id: Task ID that was not found

    Returns:
        Formatted error string
    """
    message = f"Task #{task_id} does not exist in the system."
    suggestions = [
        "Verify the task ID is correct",
        "Type '/tasks' to see all your tasks",
        "Create this task if it doesn't exist"
    ]
    return format_error("Task Not Found", message, suggestions)


def error_invalid_title() -> str:
    """
    Format invalid title error.

    Returns:
        Formatted error string
    """
    message = "The task title cannot be empty or contain only whitespace."
    suggestions = [
        "Provide a descriptive title like 'Buy groceries'",
        "Use at least 1 character",
        "Avoid using only numbers or special characters"
    ]
    return format_error("Invalid Task Title", message, suggestions)


def error_title_too_long(length: int) -> str:
    """
    Format title too long error.

    Args:
        length: Actual length of title

    Returns:
        Formatted error string
    """
    message = f"Title is too long ({length} characters). Maximum 200 characters allowed."
    suggestions = [
        "Shorten your title",
        "Use abbreviations if needed",
        "Split long tasks into multiple smaller tasks"
    ]
    return format_error("Invalid Task Title", message, suggestions)


def error_invalid_task_id(input_value: str) -> str:
    """
    Format invalid task ID error (non-numeric).

    Args:
        input_value: The invalid input value

    Returns:
        Formatted error string
    """
    message = f"Invalid task ID: '{input_value}'. Expected a number."
    suggestions = [
        "Enter a positive number (e.g., 1, 2, 3)",
        "View all tasks to see valid IDs",
        "Type '/tasks' to see your task list"
    ]
    return format_error("Invalid Task ID", message, suggestions)


def error_invalid_menu_selection(selection: str, max_option: int) -> str:
    """
    Format invalid menu selection error.

    Args:
        selection: Invalid selection value
        max_option: Maximum valid option

    Returns:
        Formatted error string
    """
    message = f"Invalid selection: '{selection}'"
    suggestions = [
        f"Choose between 1 and {max_option}",
        "Type the number of your desired option",
        "Press Enter after typing your choice"
    ]
    return format_error("Invalid Selection", message, suggestions)


def error_invalid_state_transition(task_id: int, current_state: str, timestamp: str = None) -> str:
    """
    Format invalid state transition error.

    Args:
        task_id: Task ID
        current_state: Current task status
        timestamp: Optional timestamp of when state was set

    Returns:
        Formatted error string
    """
    if current_state == "Completed":
        message = f"Task #{task_id} is already completed."
        if timestamp:
            message += f" Completed at {timestamp}"
        suggestions = [
            "Mark as incomplete: '/incomplete'",
            "View task details: '/tasks'",
            "Delete and recreate if needed"
        ]
    else:  # Already pending
        message = f"Task #{task_id} is already pending."
        suggestions = [
            "Mark as complete: '/complete'",
            "View task details: '/tasks'"
        ]
    return format_error("Invalid State Transition", message, suggestions)


def error_duplicate_task(title: str, existing_task_id: int, existing_status: str) -> str:
    """
    Format duplicate task error.

    Args:
        title: Task title that already exists
        existing_task_id: ID of existing task
        existing_status: Status of existing task

    Returns:
        Formatted error string
    """
    message = f"A task with this title already exists:\n• Task #{existing_task_id}: {title} ({existing_status})"
    suggestions = [
        f"Update existing task instead",
        f"Use a different title",
        f"Mark existing as complete if done"
    ]
    return format_error("Duplicate Task", message, suggestions)


def error_empty_input(input_type: str = "input") -> str:
    """
    Format empty input error.

    Args:
        input_type: Type of input (title, description, etc.)

    Returns:
        Formatted error string
    """
    message = f"The {input_type} cannot be empty."
    suggestions = [
        "Provide at least 1 character",
        "Avoid using only spaces",
        "Try again with valid input"
    ]
    return format_error("Empty Input", message, suggestions)
