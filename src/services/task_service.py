"""
Task service layer for Todo CLI application
Orchestrates all task operations using reusable skills
"""

from typing import Optional
from src.models.task import Task, TaskList
from src.skills.task_validation import validate_task_title, validate_task_id, validate_task_update, validate_duplicate_title
from src.skills.input_parsing import parse_menu_selection, parse_task_id, parse_text_input
from src.skills.task_formatting import format_task_list, format_single_task, format_success
from src.skills.error_handling import (
    error_task_not_found,
    error_invalid_title,
    error_invalid_task_id,
    error_invalid_state_transition,
    error_empty_input
)
from src.skills.task_state_management import transition_state, can_transition_to_completed


class TaskService:
    """
    Service layer that orchestrates task operations.
    All operations use reusable skills and return formatted responses.
    """

    def __init__(self):
        """Initialize task service with empty task list"""
        self.task_list = TaskList()

    def create_task(self, title: str, description: Optional[str] = None) -> str:
        """
        Create a new task with validation and state management.

        Args:
            title: Task title
            description: Optional task description

        Returns:
            Formatted success or error message
        """
        # Validate title
        title_result = validate_task_title(title)
        if not title_result["valid"]:
            return error_invalid_title()

        # Check for duplicate titles
        dup_result = validate_duplicate_title(title_result["normalized_title"], self.task_list)
        if not dup_result["valid"]:
            return dup_result["error"]

        # Normalize input
        normalized_title = title_result["normalized_title"]
        normalized_description = parse_text_input(description if description else "")["value"]

        # Create task with Pending status
        task = Task(
            id=0,  # Will be assigned by TaskList.add
            title=normalized_title,
            description=normalized_description if normalized_description else None,
            status="Pending"
        )

        # Add to task list
        added_task = self.task_list.add(task)

        # Format and return success message
        formatted_task = format_single_task(added_task)
        return f"{format_success('Task created successfully')}\n\n{formatted_task}"

    def view_tasks(self) -> str:
        """
        Display all tasks with metrics.

        Returns:
            Formatted task list or empty message
        """
        # Get metrics
        metrics = self.task_list.count_by_status()

        # Get all tasks
        tasks = self.task_list.list_all()

        # Format and return
        if self.task_list.is_empty():
            from src.skills.task_formatting import format_empty_list
            return format_empty_list()
        else:
            return format_task_list(tasks, metrics)

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> str:
        """
        Update an existing task.

        Args:
            task_id: Task ID to update
            title: Optional new title
            description: Optional new description

        Returns:
            Formatted success or error message
        """
        # Validate task ID exists
        id_result = validate_task_id(task_id, self.task_list)
        if not id_result["valid"]:
            return error_task_not_found(task_id)

        task = id_result["task"]

        # Validate update data
        if title is None and description is None:
            return error_empty_input("title or description")

        # Validate title if provided
        if title is not None:
            title_result = validate_task_title(title)
            if not title_result["valid"]:
                return error_invalid_title()

            # Update title
            task.title = title_result["normalized_title"]

        # Update description if provided
        if description is not None:
            desc_result = parse_text_input(description)
            if desc_result["valid"]:
                task.description = desc_result["value"]

        # Update timestamp
        from src.lib.utils import get_current_timestamp
        task.updated_at = get_current_timestamp()

        # Format and return
        formatted_task = format_single_task(task)
        return f"{format_success('Task updated successfully')}\n\n{formatted_task}"

    def delete_task(self, task_id: int, confirmed: bool = False) -> str:
        """
        Delete a task by ID.

        Args:
            task_id: Task ID to delete
            confirmed: User confirmation

        Returns:
            Formatted success or error message
        """
        # Validate task ID exists
        id_result = validate_task_id(task_id, self.task_list)
        if not id_result["valid"]:
            return error_task_not_found(task_id)

        # Check confirmation
        if not confirmed:
            task = id_result["task"]
            return f"Task deletion cancelled. Task #{task_id} not deleted.\n"

        # Delete task
        deleted = self.task_list.delete(task_id)

        if deleted:
            return f"{format_success('Task deleted successfully')}\n\nTask #{task_id} removed from your list.\n"
        else:
            return f"Task #{task_id} could not be deleted.\n"

    def mark_complete(self, task_id: int) -> str:
        """
        Mark a task as completed.

        Args:
            task_id: Task ID to mark complete

        Returns:
            Formatted success or error message
        """
        # Validate task ID exists
        id_result = validate_task_id(task_id, self.task_list)
        if not id_result["valid"]:
            return error_task_not_found(task_id)

        task = id_result["task"]

        # Validate state transition
        transition_result = transition_state(task, "Completed")
        if not transition_result["valid"]:
            # Get state description
            from src.skills.task_state_management import get_state_description
            current_desc = get_state_description(task.status)

            # Format error with suggestion
            return error_invalid_state_transition(
                task_id,
                task.status,
                task.updated_at
            )

        # Format and return success
        updated_task = transition_result["task"]
        formatted_task = format_single_task(updated_task)
        return f"{format_success('Task marked as completed')}\n\n{formatted_task}"

    def mark_incomplete(self, task_id: int) -> str:
        """
        Mark a task as incomplete (reopen).

        Args:
            task_id: Task ID to reopen

        Returns:
            Formatted success or error message
        """
        # Validate task ID exists
        id_result = validate_task_id(task_id, self.task_list)
        if not id_result["valid"]:
            return error_task_not_found(task_id)

        task = id_result["task"]

        # Validate state transition
        transition_result = transition_state(task, "Pending")
        if not transition_result["valid"]:
            # Get state description
            from src.skills.task_state_management import get_state_description
            current_desc = get_state_description(task.status)

            # Format error with suggestion
            return error_invalid_state_transition(
                task_id,
                task.status,
                task.updated_at
            )

        # Format and return success
        updated_task = transition_result["task"]
        formatted_task = format_single_task(updated_task)
        return f"{format_success('Task marked as incomplete (reopened)')}\n\n{formatted_task}"

    def get_metrics(self) -> str:
        """
        Get task count metrics.

        Returns:
            Formatted metrics string
        """
        metrics = self.task_list.count_by_status()
        return (
            f"Total: {metrics['total']} | "
            f"Pending: {metrics['pending']} | "
            f"Completed: {metrics['completed']}"
        )
