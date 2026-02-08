"""
Database configuration module.

This module configures the database connection and setup for PostgreSQL (Neon).
"""

from sqlmodel import create_engine, Session
from typing import Generator
import os
from dotenv import load_dotenv

# Import models to ensure they're registered with SQLModel
from .models.user import User
from .models.task import Task
from .models.refresh_token import RefreshToken

# Ensure relationships are properly configured
from sqlmodel import SQLModel
SQLModel.metadata.tables  # This ensures all models are registered

# Load environment variables
load_dotenv()

# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Validate that DATABASE_URL is set
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set. Please configure your Neon database URL.")

# For PostgreSQL (Neon), use the appropriate configuration
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,  # Helps with connection reliability
    pool_recycle=300,    # Recycle connections to prevent timeouts
    pool_size=10,        # Number of connections to maintain in the pool
    max_overflow=20,     # Additional connections beyond pool_size
    pool_timeout=30,     # Timeout for getting a connection from the pool
    pool_reset_on_return='commit'  # Reset connections when returned to the pool
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