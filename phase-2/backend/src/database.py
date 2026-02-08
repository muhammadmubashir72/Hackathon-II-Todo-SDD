"""
Database configuration module.

This module configures the database connection and setup for both SQLite and PostgreSQL.
"""

from sqlmodel import create_engine, Session
from typing import Generator
import os
from dotenv import load_dotenv

# Import models to ensure they're registered with SQLModel
from .models.user import User
from .models.task import Task
from .models.refresh_token import RefreshToken

# Load environment variables
load_dotenv()

# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app_dev.db")

# For SQLite, we need to handle the URL differently
if DATABASE_URL.startswith("sqlite"):
    # For SQLite, use connect_args to handle threading issues
    engine = create_engine(
        DATABASE_URL,
        echo=True,
        connect_args={"check_same_thread": False}  # Needed for SQLite
    )
else:
    # For PostgreSQL (Neon), use the appropriate configuration
    engine = create_engine(
        DATABASE_URL,
        echo=True,
        pool_pre_ping=True,  # Helps with connection reliability
        pool_recycle=300    # Recycle connections to prevent timeouts
    )


def create_tables():
    """
    Create all database tables based on registered models.
    """
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Get a database session.

    Yields:
        Database session
    """
    with Session(engine) as session:
        yield session