"""
User service module.

This module implements user management operations following the specification.
"""

from typing import Optional
from sqlmodel import Session, select
from datetime import datetime
from ..models.user import User, UserCreate
from ..skills.auth_validation import get_password_hash, validate_unique_email, validate_email_format, validate_password_strength


class UserService:
    """Service class for user operations."""

    @staticmethod
    def create_user(session: Session, user_create: UserCreate) -> User:
        """
        Create a new user with the provided data.

        Args:
            session: Database session
            user_create: User creation data

        Returns:
            Created User object

        Raises:
            ValueError: If validation fails
        """
        # Validate email format
        is_valid, error_msg = validate_email_format(user_create.email)
        if not is_valid:
            raise ValueError(error_msg)

        # Validate password strength
        is_valid, error_msg = validate_password_strength(user_create.password)
        if not is_valid:
            raise ValueError(error_msg)

        # Validate email uniqueness
        is_unique, error_msg = validate_unique_email(session, user_create.email)
        if not is_unique:
            raise ValueError(error_msg)

        # Ensure password complies with bcrypt's 72-byte limit
        from ..skills.auth_validation import truncate_password_to_bcrypt_limit
        truncated_password = truncate_password_to_bcrypt_limit(user_create.password)
        
        # Hash the password
        password_hash = get_password_hash(truncated_password)

        # Create the user object
        user = User(
            email=user_create.email.lower(),  # Store emails in lowercase
            password_hash=password_hash,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            is_active=True
        )

        # Add to session and commit
        session.add(user)
        session.commit()
        session.refresh(user)

        return user

    @staticmethod
    def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
        """
        Retrieve a user by ID.

        Args:
            session: Database session
            user_id: ID of the user to retrieve

        Returns:
            User object if found, None otherwise
        """
        return session.get(User, user_id)

    @staticmethod
    def get_user_by_email(session: Session, email: str) -> Optional[User]:
        """
        Retrieve a user by email.

        Args:
            session: Database session
            email: Email of the user to retrieve

        Returns:
            User object if found, None otherwise
        """
        statement = select(User).where(User.email == email.lower())
        return session.exec(statement).first()

    @staticmethod
    def update_user(session: Session, user_id: int, email: Optional[str] = None) -> Optional[User]:
        """
        Update user information.

        Args:
            session: Database session
            user_id: ID of the user to update
            email: New email (optional)

        Returns:
            Updated User object if successful, None if user not found

        Raises:
            ValueError: If validation fails
        """
        user = session.get(User, user_id)
        if not user:
            return None

        if email is not None:
            # Validate email format
            is_valid, error_msg = validate_email_format(email)
            if not is_valid:
                raise ValueError(error_msg)

            # Validate email uniqueness (excluding current user)
            is_unique, error_msg = validate_unique_email(session, email, exclude_user_id=user_id)
            if not is_unique:
                raise ValueError(error_msg)

            user.email = email.lower()

        user.updated_at = datetime.utcnow()
        session.add(user)
        session.commit()
        session.refresh(user)

        return user

    @staticmethod
    def deactivate_user(session: Session, user_id: int) -> bool:
        """
        Deactivate a user account.

        Args:
            session: Database session
            user_id: ID of the user to deactivate

        Returns:
            True if successful, False if user not found
        """
        user = session.get(User, user_id)
        if not user:
            return False

        user.is_active = False
        user.updated_at = datetime.utcnow()
        session.add(user)
        session.commit()
        session.refresh(user)

        return True

    @staticmethod
    def activate_user(session: Session, user_id: int) -> bool:
        """
        Activate a user account.

        Args:
            session: Database session
            user_id: ID of the user to activate

        Returns:
            True if successful, False if user not found
        """
        user = session.get(User, user_id)
        if not user:
            return False

        user.is_active = True
        user.updated_at = datetime.utcnow()
        session.add(user)
        session.commit()
        session.refresh(user)

        return True