"""
Task entity and TaskList collection for Todo CLI application
Defines core data model with validation rules and state transitions
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, List
from src.lib.utils import get_current_timestamp


@dataclass
class Task:
    """
    Represents a single todo item that users create, track, and complete.

    Attributes:
        id: Unique sequential identifier (1, 2, 3, ...)
        title: Descriptive task title (max 200 characters)
        description: Optional detailed description
        status: Task state ("Pending" or "Completed")
        created_at: Timestamp when task was created (ISO 8601 format)
        updated_at: Timestamp when task status changed (ISO 8601 format)
    """

    id: int
    title: str
    description: Optional[str] = None
    status: str = "Pending"
    created_at: str = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        """Validate task attributes after initialization"""
        if self.created_at is None:
            self.created_at = get_current_timestamp()

        # Validate status
        if self.status not in ["Pending", "Completed"]:
            raise ValueError(f"Invalid status: {self.status}. Must be 'Pending' or 'Completed'")

        # Validate title length
        if not self.title or len(self.title.strip()) == 0:
            raise ValueError("Title cannot be empty or whitespace-only")
        if len(self.title) > 200:
            raise ValueError("Title cannot exceed 200 characters")

    def to_dict(self) -> Dict:
        """Convert task to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }


class TaskList:
    """
    Collection of all tasks managed by the application.
    Maintains task count metrics and provides methods for task management.
    """

    def __init__(self):
        """Initialize empty task list"""
        self.tasks: List[Task] = []
        self._next_id: int = 1

    def add(self, task: Task) -> Task:
        """
        Add a new task to the list.
        Assigns sequential ID and Pending status.

        Args:
            task: Task object to add

        Returns:
            Task: Added task with assigned ID
        """
        task.id = self._next_id
        self._next_id += 1
        self.tasks.append(task)
        return task

    def get_by_id(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by sequential ID.
        Task ID 1 corresponds to index 0.

        Args:
            task_id: Sequential task ID (1, 2, 3, ...)

        Returns:
            Task if found, None otherwise
        """
        # Convert task_id to zero-based index
        index = task_id - 1
        if 0 <= index < len(self.tasks):
            return self.tasks[index]
        return None

    def update(self, task_id: int, **updates) -> Optional[Task]:
        """
        Update task attributes.

        Args:
            task_id: Sequential task ID to update
            **updates: Key-value pairs of attributes to update
                      (title, description, status, updated_at)

        Returns:
            Updated task if found, None otherwise
        """
        task = self.get_by_id(task_id)
        if task:
            for key, value in updates.items():
                if hasattr(task, key):
                    setattr(task, key, value)
        return task

    def delete(self, task_id: int) -> bool:
        """
        Delete a task from the list.

        Args:
            task_id: Sequential task ID to delete

        Returns:
            bool: True if deleted, False if not found
        """
        index = task_id - 1
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            return True
        return False

    def list_all(self) -> List[Task]:
        """
        Get all tasks in order of creation.

        Returns:
            List of all tasks
        """
        return self.tasks.copy()

    def count_by_status(self) -> Dict[str, int]:
        """
        Get task count metrics by status.

        Returns:
            Dictionary with keys: total, pending, completed
        """
        total = len(self.tasks)
        pending = sum(1 for task in self.tasks if task.status == "Pending")
        completed = sum(1 for task in self.tasks if task.status == "Completed")

        return {
            "total": total,
            "pending": pending,
            "completed": completed
        }

    def is_empty(self) -> bool:
        """
        Check if task list is empty.

        Returns:
            bool: True if no tasks, False otherwise
        """
        return len(self.tasks) == 0
