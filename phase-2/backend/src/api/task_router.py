"""
Task router module.

This module implements task CRUD endpoints with auth middleware following the API contracts.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from ..database import get_session
from ..models.task import TaskCreate, TaskUpdate, TaskResponse
from ..services.task_service import TaskService
from ..middleware.auth_middleware import auth_middleware
from ..skills.input_parsing import parse_task_input
from ..skills.task_formatting import format_task_response, format_tasks_list_response
from ..skills.task_validation import validate_user_ownership
from ..skills.error_handling import handle_validation_error, handle_authentication_error, handle_permission_denied, handle_not_found, handle_conflict, handle_internal_error


task_router = APIRouter(prefix="/tasks", tags=["Tasks"])


@task_router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_create: TaskCreate,
    current_user_id: int = Depends(auth_middleware.get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.

    Args:
        task_create: Task creation data
        current_user_id: ID of the authenticated user
        session: Database session

    Returns:
        Created task data
    """
    try:
        # Parse and normalize input
        parsed_data = parse_task_input(task_create.model_dump())

        # Create task through service
        task = TaskService.create_task(
            session,
            TaskCreate(**parsed_data),
            current_user_id
        )

        # Format and return response
        return format_task_response(task)

    except ValueError as e:
        raise handle_validation_error(str(e))
    except Exception as e:
        import traceback
        print(f"Task creation error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise handle_internal_error(f"Task creation failed: {str(e)}")


@task_router.get("", response_model=dict)
def get_tasks(
    limit: int = 50,
    offset: int = 0,
    status_filter: str = "all",
    current_user_id: int = Depends(auth_middleware.get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the authenticated user.

    Args:
        limit: Number of tasks to return
        offset: Number of tasks to skip
        status_filter: Filter by completion status
        current_user_id: ID of the authenticated user
        session: Database session

    Returns:
        List of tasks with pagination info
    """
    try:
        # Validate query parameters
        if limit < 1 or limit > 100:
            limit = 50
        if offset < 0:
            offset = 0
        if status_filter not in ["all", "pending", "completed"]:
            status_filter = "all"

        # Get tasks through service
        tasks = TaskService.get_tasks_for_user(
            session,
            current_user_id,
            limit,
            offset,
            status_filter
        )

        # Get total count for pagination
        total_count = TaskService.get_total_task_count(session, current_user_id, status_filter)

        # Format and return response
        return format_tasks_list_response(tasks, total_count, limit, offset)

    except Exception as e:
        raise handle_validation_error("Failed to retrieve tasks")


@task_router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current_user_id: int = Depends(auth_middleware.get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID.

    Args:
        task_id: ID of the task to retrieve
        current_user_id: ID of the authenticated user
        session: Database session

    Returns:
        Task data
    """
    try:
        # Get task through service
        task = TaskService.get_task_by_id(session, task_id, current_user_id)

        if not task:
            raise handle_not_found("Task not found")

        # Format and return response
        return format_task_response(task)

    except Exception as e:
        raise handle_not_found("Task not found")


@task_router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user_id: int = Depends(auth_middleware.get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Update an existing task.

    Args:
        task_id: ID of the task to update
        task_update: Task update data
        current_user_id: ID of the authenticated user
        session: Database session

    Returns:
        Updated task data
    """
    try:
        # Parse and normalize input
        parsed_data = parse_task_input(task_update.model_dump())

        # Update task through service
        updated_task = TaskService.update_task(
            session,
            task_id,
            TaskUpdate(**parsed_data),
            current_user_id
        )

        if not updated_task:
            raise handle_not_found("Task not found")

        # Format and return response
        return format_task_response(updated_task)

    except ValueError as e:
        raise handle_validation_error(str(e))
    except Exception as e:
        import traceback
        print(f"Task update error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise handle_internal_error(f"Task update failed: {str(e)}")


@task_router.delete("/{task_id}")
def delete_task(
    task_id: int,
    current_user_id: int = Depends(auth_middleware.get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task.

    Args:
        task_id: ID of the task to delete
        current_user_id: ID of the authenticated user
        session: Database session

    Returns:
        Success message
    """
    try:
        # Delete task through service
        success = TaskService.delete_task(session, task_id, current_user_id)

        if not success:
            raise handle_not_found("Task not found")

        return {"message": "Task deleted successfully"}

    except Exception as e:
        raise handle_not_found("Task not found")