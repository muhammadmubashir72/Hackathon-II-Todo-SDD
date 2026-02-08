"""
Authentication router module.

This module implements authentication endpoints (register, login, logout, refresh) following the API contracts.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from jose import jwt
from sqlmodel import Session
from typing import Optional
import os
from dotenv import load_dotenv
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..database import get_session
from ..models.user import UserCreate, UserLogin, UserResponse
from ..services.user_service import UserService
from ..services.refresh_token_service import RefreshTokenService
from ..skills.auth_validation import validate_user_credentials, create_access_token, create_access_token_default, create_refresh_token
from ..skills.input_parsing import parse_user_input
from ..skills.task_formatting import format_token_response, format_user_response
from ..skills.error_handling import handle_validation_error, handle_authentication_error

# Initialize security for logout endpoint
security = HTTPBearer()

# Load environment variables
load_dotenv()

# Get configuration from environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "your-default-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(
    user_create: UserCreate,
    session: Session = Depends(get_session)
):
    """
    Register a new user account.

    Args:
        user_create: User creation data
        session: Database session

    Returns:
        Token response with access token and user data
    """
    try:
        # Parse and normalize input
        parsed_data = parse_user_input(user_create.model_dump())

        # Create user through service
        user = UserService.create_user(session, UserCreate(**parsed_data))

        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token_default(
            data={"sub": str(user.id)},
            expires_delta=access_token_expires
        )

        # Format and return response with token
        return format_token_response(access_token, "bearer", user)

    except ValueError as e:
        raise handle_validation_error(str(e))
    except Exception as e:
        raise handle_validation_error("Registration failed")


@auth_router.post("/login")
def login_user(
    user_login: UserLogin,
    session: Session = Depends(get_session)
):
    """
    Authenticate user and return JWT tokens.

    Args:
        user_login: User login credentials
        session: Database session

    Returns:
        Token response with access token, refresh token and user data
    """
    try:
        # Validate credentials
        user, error_msg = validate_user_credentials(
            session,
            user_login.email,
            user_login.password
        )

        if not user:
            raise handle_authentication_error(error_msg or "Invalid credentials")

        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token_default(
            data={"sub": str(user.id)},
            expires_delta=access_token_expires
        )

        # Create refresh token in database (this generates the actual refresh token string)
        refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        db_refresh_token = RefreshTokenService.create_refresh_token(
            session,
            user.id,
            refresh_token_expires
        )

        # Format and return response with both tokens
        return format_token_response(access_token, "bearer", user, db_refresh_token.token)

    except Exception as e:
        raise handle_authentication_error("Login failed")


@auth_router.post("/refresh")
def refresh_token(
    refresh_token_data: dict,
    session: Session = Depends(get_session)
):
    """
    Refresh access token using refresh token.

    Args:
        refresh_token_data: Contains refresh_token string
        session: Database session

    Returns:
        New access token
    """
    try:
        refresh_token_str = refresh_token_data.get("refresh_token")
        if not refresh_token_str:
            raise handle_authentication_error("Refresh token is required")

        # Use the middleware's refresh function
        from ..middleware.auth_middleware import auth_middleware
        result = auth_middleware.refresh_access_token(refresh_token_str, session)

        if not result:
            raise handle_authentication_error("Invalid or expired refresh token")

        return result

    except Exception as e:
        raise handle_authentication_error("Token refresh failed")


@auth_router.post("/logout")
def logout_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
):
    """
    Logout current user and invalidate refresh tokens.

    Args:
        credentials: HTTP authorization credentials
        session: Database session

    Returns:
        Success message
    """
    try:
        # Extract user ID from token
        token = credentials.credentials
        from ..skills.auth_validation import verify_token
        payload = verify_token(token, SECRET_KEY)

        if payload:
            user_id = int(payload.get("sub"))
            # Revoke all refresh tokens for this user
            RefreshTokenService.revoke_all_user_refresh_tokens(session, user_id)

        return {"message": "Successfully logged out"}
    except Exception:
        # Even if there's an error revoking tokens, still return success
        return {"message": "Successfully logged out"}