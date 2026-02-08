"""
User model module.

This module defines the User entity model with authentication following the specification.
"""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
import uuid


class User(SQLModel, table=True):
    """
    User model representing a registered user with unique identifier,
    email address, encrypted password, account creation timestamp,
    and authentication status.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, nullable=False, max_length=254)
    password_hash: str = Field(nullable=False)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

    # Relationships to tasks and refresh tokens
    tasks: List["Task"] = Relationship(back_populates="user")
    refresh_tokens: List["RefreshToken"] = Relationship(back_populates="user")


# Model for creating new users (without ID)
class UserCreate(SQLModel):
    """Model for creating new users."""
    email: str
    password: str


# Model for user login
class UserLogin(SQLModel):
    """Model for user login."""
    email: str
    password: str


# Model for user response (without sensitive data)
class UserResponse(SQLModel):
    """Model for user response without sensitive data."""
    id: int
    email: str
    created_at: datetime
    updated_at: datetime
    is_active: bool