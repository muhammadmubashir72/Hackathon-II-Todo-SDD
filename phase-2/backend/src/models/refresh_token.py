"""
Refresh token model module.

This module defines the RefreshToken entity model with relationships.
"""

from datetime import datetime
from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

if TYPE_CHECKING:
    from .user import User


class RefreshToken(SQLModel, table=True):
    """
    Refresh token model representing a refresh token entity.

    Attributes:
        id: Unique identifier for the refresh token
        token: The refresh token string
        user_id: Foreign key to the user who owns this token
        expires_at: Expiration timestamp for the token
        created_at: Creation timestamp
        is_active: Whether the token is currently valid
        user: Relationship to the associated user
    """
    __tablename__ = "refresh_tokens"

    id: int = Field(default=None, primary_key=True)
    token: str = Field(unique=True, index=True)
    user_id: int = Field(foreign_key="user.id")
    expires_at: datetime = Field(sa_column=Column(DateTime(timezone=True)))
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True)), default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

    # Relationship to user
    user: "User" = Relationship(back_populates="refresh_tokens")


class RefreshTokenCreate(SQLModel):
    """
    Schema for creating a new refresh token.

    Attributes:
        token: The refresh token string
        user_id: ID of the user this token belongs to
        expires_at: When the token expires
    """
    token: str
    user_id: int
    expires_at: datetime


class RefreshTokenResponse(SQLModel):
    """
    Schema for refresh token API responses.

    Attributes:
        id: The refresh token ID
        token: The refresh token string (should not be exposed in production)
        user_id: ID of the user this token belongs to
        expires_at: When the token expires
        created_at: When the token was created
        is_active: Whether the token is currently valid
    """
    id: int
    user_id: int
    expires_at: datetime
    created_at: datetime
    is_active: bool