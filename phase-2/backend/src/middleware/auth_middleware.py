"""
Authentication middleware module.

This module creates authentication middleware for JWT token validation.
"""

from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, Any, Optional
from datetime import timedelta
import os
from jose import JWTError, jwt
from dotenv import load_dotenv
from sqlmodel import Session
from ..database import get_session
from ..models.user import User
from ..skills.auth_validation import verify_token, validate_jwt_payload, create_access_token, create_refresh_token

# Load environment variables
load_dotenv()

# Get secret key from environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "your-default-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))

security = HTTPBearer()


class AuthMiddleware:
    """Authentication middleware class for JWT token validation."""

    @staticmethod
    async def verify_token_from_request(
        request: Request,
        credentials: HTTPAuthorizationCredentials = Depends(security),
        session: Session = Depends(get_session)
    ) -> Dict[str, Any]:
        """
        Verify JWT token from request headers.

        Args:
            request: FastAPI request object
            credentials: HTTP authorization credentials
            session: Database session

        Returns:
            Token payload dictionary

        Raises:
            HTTPException: If token is invalid or expired
        """
        token = credentials.credentials

        # Verify the token
        payload = verify_token(token, SECRET_KEY)
        if payload is None:
            raise HTTPException(
                status_code=401,
                detail={"error": "Invalid authentication credentials"}
            )

        # Validate the payload
        is_valid, error_msg = validate_jwt_payload(payload)
        if not is_valid:
            raise HTTPException(
                status_code=401,
                detail={"error": error_msg}
            )

        # Check if user exists in database
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail={"error": "Could not validate credentials"}
            )

        # Verify user exists and is active
        user = session.get(User, user_id)
        if user is None or not user.is_active:
            raise HTTPException(
                status_code=401,
                detail={"error": "User no longer exists or is inactive"}
            )

        return payload

    @staticmethod
    async def get_current_user_id(
        request: Request,
        session: Session = Depends(get_session)
    ) -> int:
        """
        Get current user ID from token payload.

        Args:
            request: FastAPI request object
            session: Database session

        Returns:
            Current user ID
        """
        # Extract and verify token manually
        auth_header = request.headers.get("authorization")
        if not auth_header:
            raise HTTPException(
                status_code=401,
                detail={"error": "Not authenticated"}
            )

        try:
            scheme, token = auth_header.split(" ", 1)
            if scheme.lower() != "bearer":
                raise HTTPException(
                    status_code=401,
                    detail={"error": "Invalid authentication scheme"}
                )
        except ValueError:
            raise HTTPException(
                status_code=401,
                detail={"error": "Invalid authorization header format"}
            )

        # Verify the token
        payload = verify_token(token, SECRET_KEY)
        if payload is None:
            raise HTTPException(
                status_code=401,
                detail={"error": "Invalid authentication credentials"}
            )

        # Validate the payload
        is_valid, error_msg = validate_jwt_payload(payload)
        if not is_valid:
            raise HTTPException(
                status_code=401,
                detail={"error": error_msg}
            )

        # Get user ID from payload
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail={"error": "Could not validate credentials"}
            )

        # Verify user exists and is active
        user = session.get(User, user_id)
        if user is None or not user.is_active:
            raise HTTPException(
                status_code=401,
                detail={"error": "User no longer exists or is inactive"}
            )

        return int(user_id)

    @staticmethod
    async def optional_auth(
        request: Request,
        session: Session = Depends(get_session)
    ) -> Optional[Dict[str, Any]]:
        """
        Optional authentication - doesn't raise exception if no token provided.

        Args:
            request: FastAPI request object
            session: Database session

        Returns:
            Token payload dictionary or None if no valid token
        """
        # Extract authorization header manually
        auth_header = request.headers.get("authorization")
        if not auth_header:
            return None

        # Parse the header
        try:
            scheme, token = auth_header.split(" ", 1)
            if scheme.lower() != "bearer":
                return None
        except ValueError:
            return None

        payload = verify_token(token, SECRET_KEY)

        if payload is None:
            return None

        is_valid, error_msg = validate_jwt_payload(payload)
        if not is_valid:
            return None

        user_id = payload.get("sub")
        if user_id is None:
            return None

        user = session.get(User, user_id)
        if user is None or not user.is_active:
            return None

        return payload

    @staticmethod
    def refresh_access_token(
        refresh_token_str: str,
        session: Session = Depends(get_session)
    ) -> Optional[Dict[str, str]]:
        """
        Refresh an access token using a refresh token.

        Args:
            refresh_token_str: The refresh token string
            session: Database session

        Returns:
            Dictionary with new access token if successful, None otherwise
        """
        from ..services.refresh_token_service import RefreshTokenService

        # Get the refresh token from the database
        refresh_token_obj = RefreshTokenService.get_refresh_token_by_token(session, refresh_token_str)

        if not refresh_token_obj:
            return None

        # Verify the user still exists and is active
        user = session.get(User, refresh_token_obj.user_id)
        if not user or not user.is_active:
            # Revoke the refresh token if user is inactive
            RefreshTokenService.revoke_refresh_token(session, refresh_token_str)
            return None

        # Create new access token
        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        return {"access_token": access_token, "token_type": "bearer"}


# Create instance of auth middleware
auth_middleware = AuthMiddleware()