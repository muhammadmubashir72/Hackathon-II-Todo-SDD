"""
Authentication and authorization validation skill module.

This module handles user identification, permission checking, and data access control following the reusable skills architecture.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import re
from sqlmodel import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from ..models.user import User


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a hashed password.

    Args:
        plain_password: Plaintext password to verify
        hashed_password: Hashed password to compare against

    Returns:
        Boolean indicating if passwords match
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Generate a hash for a plaintext password.

    Args:
        password: Plaintext password to hash

    Returns:
        Hashed password string
    """
    return pwd_context.hash(password)


def validate_email_format(email: str) -> tuple[bool, Optional[str]]:
    """
    Validate email format according to RFC standards.

    Args:
        email: Email address to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if not email or not isinstance(email, str):
        return False, "Email cannot be empty or None"

    if not re.match(pattern, email):
        return False, "Invalid email format"

    if len(email) > 254:  # RFC 5321 limit
        return False, "Email address too long"

    return True, None


def validate_password_strength(password: str) -> tuple[bool, Optional[str]]:
    """
    Validate password strength according to security requirements.

    Args:
        password: Password to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not password or not isinstance(password, str):
        return False, "Password cannot be empty or None"

    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if len(password) > 128:  # Reasonable upper limit
        return False, "Password must be no more than 128 characters long"

    # Check for at least one lowercase, uppercase, digit, and special character
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    if not (has_lower and has_upper and has_digit):
        return False, "Password must contain at least one lowercase letter, one uppercase letter, and one digit"

    return True, None


def validate_user_credentials(
    session: Session,
    email: str,
    password: str
) -> tuple[Optional[User], Optional[str]]:
    """
    Validate user credentials against stored user data.

    Args:
        session: Database session
        email: User email address
        password: User password

    Returns:
        Tuple of (user_object, error_message)
    """
    from sqlmodel import select

    # Validate email format first
    is_valid, error_msg = validate_email_format(email)
    if not is_valid:
        return None, error_msg

    # Find user by email
    statement = select(User).where(User.email == email.lower())
    user = session.exec(statement).first()
    if not user:
        return None, "Invalid credentials"

    # Check if user is active
    if not user.is_active:
        return None, "Account is deactivated"

    # Verify password
    if not verify_password(password, user.password_hash):
        return None, "Invalid credentials"

    return user, None


def create_access_token(data: Dict[str, Any], secret_key: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: Data to encode in the token
        secret_key: Secret key for signing the token
        expires_delta: Optional expiration time delta

    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Default to 30 minutes if no expiration is provided
        expire = datetime.utcnow() + timedelta(minutes=30)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm="HS256")
    return encoded_jwt


def create_access_token_default(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token using the default secret key from environment.

    Args:
        data: Data to encode in the token
        expires_delta: Optional expiration time delta

    Returns:
        Encoded JWT token string
    """
    import os
    secret_key = os.getenv("SECRET_KEY", "your-default-secret-key-change-in-production")
    return create_access_token(data, secret_key, expires_delta)


def create_refresh_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT refresh token.

    Args:
        data: Data to encode in the token
        expires_delta: Optional expiration time delta

    Returns:
        Encoded JWT refresh token string
    """
    import os
    secret_key = os.getenv("SECRET_KEY", "your-default-secret-key-change-in-production")

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Default to 7 days for refresh tokens
        expire = datetime.utcnow() + timedelta(days=7)

    to_encode.update({"exp": expire, "type": "refresh"})

    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm="HS256")
    return encoded_jwt


def verify_token(token: str, secret_key: str) -> Optional[Dict[str, Any]]:
    """
    Verify a JWT token and return its payload.

    Args:
        token: JWT token string to verify
        secret_key: Secret key used for verification

    Returns:
        Token payload dictionary or None if invalid
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except JWTError:
        return None


def validate_user_authorization(
    session: Session,
    user_id: int,
    resource_owner_id: int
) -> tuple[bool, Optional[str]]:
    """
    Validate that a user is authorized to access a resource.

    Args:
        session: Database session
        user_id: ID of the requesting user
        resource_owner_id: ID of the resource owner

    Returns:
        Tuple of (is_authorized, error_message)
    """
    # In a multi-tenant system, users can only access their own resources
    if user_id != resource_owner_id:
        return False, "Access denied: Resource belongs to another user"

    # Additional authorization checks can be added here

    return True, None


def validate_user_exists(session: Session, user_id: int) -> tuple[bool, Optional[str]]:
    """
    Validate that a user exists in the system.

    Args:
        session: Database session
        user_id: ID of the user to check

    Returns:
        Tuple of (exists, error_message)
    """
    user = session.get(User, user_id)
    if not user:
        return False, "User not found"

    if not user.is_active:
        return False, "User account is deactivated"

    return True, None


def validate_unique_email(session: Session, email: str, exclude_user_id: Optional[int] = None) -> tuple[bool, Optional[str]]:
    """
    Validate that an email is unique in the system.

    Args:
        session: Database session
        email: Email to validate for uniqueness
        exclude_user_id: Optional user ID to exclude from check (for updates)

    Returns:
        Tuple of (is_unique, error_message)
    """
    from sqlmodel import select

    statement = select(User).where(User.email == email.lower())

    if exclude_user_id is not None:
        statement = statement.where(User.id != exclude_user_id)

    existing_user = session.exec(statement).first()

    if existing_user:
        return False, "Email is already registered"

    return True, None


def validate_jwt_payload(payload: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """
    Validate JWT payload structure and content.

    Args:
        payload: JWT payload to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not isinstance(payload, dict):
        return False, "Invalid token payload format"

    # Check for required fields
    required_fields = ["sub", "exp"]
    for field in required_fields:
        if field not in payload:
            return False, f"Token payload missing required field: {field}"

    # Validate expiration
    exp_timestamp = payload.get("exp")
    if exp_timestamp:
        if isinstance(exp_timestamp, (int, float)):
            if datetime.utcfromtimestamp(exp_timestamp) < datetime.utcnow():
                return False, "Token has expired"
        else:
            return False, "Invalid expiration timestamp in token"

    return True, None