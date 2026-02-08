"""
Task service module.

This module implements task CRUD operations with user isolation following the specification.
"""

from typing import List, Optional
from sqlmodel import Session, select
from datetime import datetime
from ..models.task import Task, TaskCreate, TaskUpdate
from ..models.user import User
from ..skills.task_validation import validate_task_title, validate_task_description
from ..skills.task_state_management import update_task_completion_status


class TaskService:
    """Service class for task operations with user isolation."""

    @staticmethod
    def create_task(session: Session, task_create: TaskCreate, user_id: int) -> Task:
        """
        Create a new task for the specified user.

        Args:
            session: Database session
            task_create: Task creation data
            user_id: ID of the user creating the task

        Returns:
            Created Task object

        Raises:
            ValueError: If validation fails
        """
        # Validate task title
        is_valid, error_msg = validate_task_title(task_create.title)
        if not is_valid:
            raise ValueError(error_msg)

        # Validate task description if provided
        if task_create.description:
            is_valid, error_msg = validate_task_description(task_create.description)
            if not is_valid:
                raise ValueError(error_msg)

        # Create the task object
        task = Task(
            title=task_create.title,
            description=task_create.description,
            is_completed=False,  # New tasks are initially pending
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            due_date=task_create.due_date,
            status=task_create.status if task_create.status is not None else "todo",
            priority=task_create.priority if task_create.priority is not None else "medium",
            category=task_create.category,
            tags=','.join(task_create.tags) if isinstance(task_create.tags, list) else task_create.tags,
            user_id=user_id
        )

        # Add to session and commit
        session.add(task)
        session.commit()
        session.refresh(task)

        return task

    @staticmethod
    def get_task_by_id(session: Session, task_id: int, user_id: int) -> Optional[Task]:
        """
        Retrieve a task by ID for the specified user.

        Args:
            session: Database session
            task_id: ID of the task to retrieve
            user_id: ID of the user requesting the task

        Returns:
            Task object if found and owned by user, None otherwise
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        return session.exec(statement).first()

    @staticmethod
    def get_tasks_for_user(
        session: Session,
        user_id: int,
        limit: int = 50,
        offset: int = 0,
        status: str = "all"
    ) -> List[Task]:
        """
        Retrieve tasks for the specified user with optional filtering and pagination.

        Args:
            session: Database session
            user_id: ID of the user whose tasks to retrieve
            limit: Maximum number of tasks to return
            offset: Number of tasks to skip
            status: Filter by status ("all", "pending", "completed")

        Returns:
            List of Task objects
        """
        statement = select(Task).where(Task.user_id == user_id)

        if status == "pending":
            statement = statement.where(Task.is_completed == False)
        elif status == "completed":
            statement = statement.where(Task.is_completed == True)

        statement = statement.offset(offset).limit(limit)
        return session.exec(statement).all()

    @staticmethod
    def update_task(
        session: Session,
        task_id: int,
        task_update: TaskUpdate,
        user_id: int
    ) -> Optional[Task]:
        """
        Update a task for the specified user.

        Args:
            session: Database session
            task_id: ID of the task to update
            task_update: Task update data
            user_id: ID of the user updating the task

        Returns:
            Updated Task object if successful, None if task not found or not owned by user

        Raises:
            ValueError: If validation fails
        """
        # Retrieve the task to ensure it exists and belongs to the user
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            return None

        # Validate and update title if provided
        if task_update.title is not None:
            is_valid, error_msg = validate_task_title(task_update.title)
            if not is_valid:
                raise ValueError(error_msg)
            task.title = task_update.title

        # Validate and update description if provided
        if task_update.description is not None:
            if task_update.description:
                is_valid, error_msg = validate_task_description(task_update.description)
                if not is_valid:
                    raise ValueError(error_msg)
            task.description = task_update.description

        # Update completion status if provided
        if task_update.is_completed is not None:
            # Only validate state transition if the status is actually changing
            if task.is_completed != task_update.is_completed:
                # Use the state management skill to update completion status
                try:
                    task = update_task_completion_status(session, task_id, task_update.is_completed)
                except ValueError as e:
                    raise ValueError(str(e))
            # If status is not changing, we don't need to do anything special
            # The task.is_completed is already the correct value

        # Update due date if provided
        if task_update.due_date is not None:
            task.due_date = task_update.due_date

        # Update status if provided
        if task_update.status is not None:
            task.status = task_update.status

        # Update priority if provided
        if task_update.priority is not None:
            task.priority = task_update.priority

        # Update category if provided
        if task_update.category is not None:
            task.category = task_update.category

        # Update tags if provided
        if task_update.tags is not None:
            if isinstance(task_update.tags, list):
                task.tags = ','.join(task_update.tags)
            else:
                task.tags = task_update.tags

        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)

        return task

    @staticmethod
    def delete_task(session: Session, task_id: int, user_id: int) -> bool:
        """
        Delete a task for the specified user.

        Args:
            session: Database session
            task_id: ID of the task to delete
            user_id: ID of the user deleting the task

        Returns:
            True if successful, False if task not found or not owned by user
        """
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            return False

        session.delete(task)
        session.commit()

        return True

    @staticmethod
    def get_total_task_count(session: Session, user_id: int, status: str = "all") -> int:
        """
        Get the total count of tasks for a user with optional status filtering.

        Args:
            session: Database session
            user_id: ID of the user
            status: Filter by status ("all", "pending", "completed")

        Returns:
            Total count of tasks matching criteria
        """
        from sqlmodel import func

        statement = select(func.count(Task.id)).where(Task.user_id == user_id)

        if status == "pending":
            statement = statement.where(Task.is_completed == False)
        elif status == "completed":
            statement = statement.where(Task.is_completed == True)

        return session.exec(statement).one()

    @staticmethod
    def toggle_task_completion(session: Session, task_id: int, user_id: int) -> Optional[Task]:
        """
        Toggle the completion status of a task.

        Args:
            session: Database session
            task_id: ID of the task to toggle
            user_id: ID of the user toggling the task

        Returns:
            Updated Task object if successful, None if task not found or not owned by user
        """
        task = session.get(Task, task_id)
        if not task or task.user_id != user_id:
            return None

        # Toggle the completion status
        new_status = not task.is_completed

        # Only validate state transition if the status is actually changing
        if task.is_completed != new_status:
            # Use the state management skill to update completion status
            try:
                task = update_task_completion_status(session, task_id, new_status)
            except ValueError as e:
                raise ValueError(str(e))
        # If status is not changing (shouldn't happen with toggle, but just in case), 
        # just update the timestamp
        task.updated_at = datetime.utcnow()

        session.add(task)
        session.commit()
        session.refresh(task)

        return task