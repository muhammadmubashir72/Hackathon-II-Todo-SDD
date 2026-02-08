"""
Task model module.

This module defines the Task entity model with user relationship following the specification.
"""

from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional
from datetime import datetime
from enum import Enum


class TaskStatus(str, Enum):
    """Enum for task status values."""
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    REVIEW = "review"
    DONE = "done"


class TaskPriority(str, Enum):
    """Enum for task priority values."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


if TYPE_CHECKING:
    from .user import User


class Task(SQLModel, table=True):
    """
    Task model representing a todo item owned by a specific user,
    containing unique identifier, title, description, completion status,
    creation timestamp, completion timestamp (when applicable),
    and foreign key linking to the owning User.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_completed: bool = Field(default=False)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = Field(default=None)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    # New fields
    due_date: Optional[datetime] = Field(default=None)
    status: TaskStatus = Field(default=TaskStatus.TODO)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)
    category: Optional[str] = Field(default=None, max_length=100)
    tags: Optional[str] = Field(default=None)  # Store as comma-separated string

    # Foreign key to User
    user_id: int = Field(foreign_key="user.id")

    # Relationship to user
    user: Optional["User"] = Relationship(back_populates="tasks")


# Model for creating new tasks
class TaskCreate(SQLModel):
    """Model for creating new tasks."""
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    category: Optional[str] = None
    tags: Optional[str] = None


# Model for updating tasks
class TaskUpdate(SQLModel):
    """Model for updating tasks."""
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    due_date: Optional[datetime] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    category: Optional[str] = None
    tags: Optional[str] = None


# Model for task response
class TaskResponse(SQLModel):
    """Model for task response."""
    id: int
    title: str
    description: Optional[str]
    is_completed: bool
    created_at: datetime
    completed_at: Optional[datetime]
    updated_at: datetime
    user_id: int
    # New fields
    due_date: Optional[datetime] = None
    status: TaskStatus
    priority: TaskPriority
    category: Optional[str] = None
    tags: Optional[str] = None