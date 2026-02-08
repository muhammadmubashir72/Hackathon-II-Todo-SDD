"""
Task formatting skill for Todo CLI application
Defines how task data is presented to the user
"""

from typing import Dict, List, Any
from src.models.task import Task


def format_task_list(tasks: List[Task], metrics: Dict[str, int]) -> str:
    """
    Format task list with clean, readable layout.

    Args:
        tasks: List of tasks to display
        metrics: Task count metrics (total, pending, completed)

    Returns:
        Formatted string ready for display
    """
    if not tasks:
        return format_empty_list()

    separator = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    header = f"\n{separator}\n  Your Tasks ({metrics['total']})\n{separator}\n"

    task_lines = []
    for task in tasks:
        status_icon = "[✓]" if task.status == "Completed" else "[ ]"
        task_line = f"  {status_icon} Task #{task.id}: {task.title}\n"
        task_line += f"      Status: {task.status}\n"
        task_line += f"      Created: {format_timestamp(task.created_at)}\n"
        task_lines.append(task_line)

    footer = f"{separator}\n"

    return header + "".join(task_lines) + footer


def format_empty_list() -> str:
    """
    Format empty task list with helpful message.

    Returns:
        Formatted string ready for display
    """
    separator = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    header = f"\n{separator}\n  No Tasks Found\n{separator}\n"
    message = "You don't have any tasks yet.\n"
    suggestion = "Would you like to create one? (1) Yes / (2) No\n"
    footer = f"{separator}\n"

    return header + message + suggestion + footer


def format_single_task(task: Task) -> str:
    """
    Format single task for display after operations.

    Args:
        task: Task to format

    Returns:
        Formatted string ready for display
    """
    separator = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    status_icon = "[✓]" if task.status == "Completed" else "[ ]"
    header = f"\n{separator}\n  Task #{task.id}: {task.title}\n{separator}\n"

    details = f"  Status: {task.status}\n"
    details += f"  Created: {format_timestamp(task.created_at)}\n"

    if task.updated_at:
        details += f"  Updated: {format_timestamp(task.updated_at)}\n"

    if task.description:
        details += f"  Description: {task.description}\n"

    return header + details


def format_timestamp(timestamp: str) -> str:
    """
    Format ISO 8601 timestamp to human-readable format.

    Args:
        timestamp: ISO 8601 timestamp string

    Returns:
        Formatted timestamp string
    """
    # Simple format: YYYY-MM-DD HH:MM
    try:
        if timestamp:
            # Extract date and time parts
            if "T" in timestamp:
                date_part, time_part = timestamp.split("T")
                date_part = date_part.replace("-", "/")
                time_part = time_part[:5]  # HH:MM only
                return f"{date_part} {time_part}"
            return timestamp
        return ""
    except Exception:
        return timestamp


def format_main_menu() -> str:
    """
    Format main menu display.

    Returns:
        Formatted menu string ready for display
    """
    separator = "━" * 60
    title = f"\n{separator}\n         Todo Console Application\n{separator}\n"
    prompt = "  Choose an option:\n\n"

    options = "  1) Add task\n"
    options += "  2) View tasks\n"
    options += "  3) Update task\n"
    options += "  4) Delete task\n"
    options += "  5) Mark complete\n"
    options += "  6) Mark incomplete\n"
    options += "  7) Exit\n"
    choice_prompt = f"\n  Your choice: "

    return title + prompt + options + choice_prompt


def format_success(message: str) -> str:
    """
    Format success message.

    Args:
        message: Success message to display

    Returns:
        Formatted success string
    """
    return f"✅ {message}\n"


def format_error(error_type: str, message: str, suggestions: List[str] = None) -> str:
    """
    Format error message with standard structure.

    Args:
        error_type: Error category/type
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
