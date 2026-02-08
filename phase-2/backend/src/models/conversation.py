"""
Conversation history model module.

This module defines the data model for storing conversation history between users and the AI assistant.
"""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from .user import User


class Conversation(SQLModel, table=True):
    """
    Conversation model representing a conversation between a user and the AI assistant.
    """
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")  # Changed from "users.id" to "user.id" to match the table name
    title: Optional[str] = Field(default="New Conversation", max_length=255)  # Optional title for the conversation
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    # Relationship with the User model
    user: Optional[User] = Relationship(back_populates="conversations")
    messages: List["Message"] = Relationship(back_populates="conversation")


class Message(SQLModel, table=True):
    """
    Message model representing individual messages in a conversation.
    """
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id")
    role: str = Field(max_length=50)  # 'user' or 'assistant'
    content: str  # The actual message content
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)
    operation_performed: Optional[str] = Field(default=None, max_length=100)  # Optional: what operation was performed

    # Relationship with the Conversation model
    conversation: Optional[Conversation] = Relationship(back_populates="messages")