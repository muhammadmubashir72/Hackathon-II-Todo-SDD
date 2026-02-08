"""
Refresh token service module.

This module implements refresh token operations following the specification.
"""

from datetime import datetime, timedelta
from typing import Optional
import secrets
from sqlmodel import Session, select
from ..models.refresh_token import RefreshToken, RefreshTokenCreate
from ..models.user import User


class RefreshTokenService:
    """Service class for handling refresh token operations."""

    @staticmethod
    def create_refresh_token(session: Session, user_id: int, expires_delta: Optional[timedelta] = None) -> RefreshToken:
        """
        Create a new refresh token for a user.

        Args:
            session: Database session
            user_id: ID of the user to create token for
            expires_delta: Optional expiration time delta (defaults to 7 days)

        Returns:
            Created RefreshToken object
        """
        if expires_delta is None:
            expires_delta = timedelta(days=7)  # Default to 7 days

        # Generate a random token
        token = secrets.token_urlsafe(32)

        # Create expiration datetime
        expires_at = datetime.utcnow() + expires_delta

        # Create refresh token object
        refresh_token = RefreshToken(
            token=token,
            user_id=user_id,
            expires_at=expires_at
        )

        # Add to database
        session.add(refresh_token)
        session.commit()
        session.refresh(refresh_token)

        return refresh_token

    @staticmethod
    def get_refresh_token_by_token(session: Session, token: str) -> Optional[RefreshToken]:
        """
        Retrieve a refresh token by its token string.

        Args:
            session: Database session
            token: The refresh token string

        Returns:
            RefreshToken object if found and valid, None otherwise
        """
        statement = select(RefreshToken).where(
            RefreshToken.token == token,
            RefreshToken.is_active == True,
            RefreshToken.expires_at > datetime.utcnow()
        )
        refresh_token = session.exec(statement).first()

        return refresh_token

    @staticmethod
    def get_refresh_token_by_id(session: Session, token_id: int) -> Optional[RefreshToken]:
        """
        Retrieve a refresh token by its ID.

        Args:
            session: Database session
            token_id: The refresh token ID

        Returns:
            RefreshToken object if found and valid, None otherwise
        """
        statement = select(RefreshToken).where(
            RefreshToken.id == token_id,
            RefreshToken.is_active == True,
            RefreshToken.expires_at > datetime.utcnow()
        )
        refresh_token = session.exec(statement).first()

        return refresh_token

    @staticmethod
    def revoke_refresh_token(session: Session, token: str) -> bool:
        """
        Revoke a refresh token by setting it as inactive.

        Args:
            session: Database session
            token: The refresh token string to revoke

        Returns:
            True if token was revoked, False if not found
        """
        statement = select(RefreshToken).where(RefreshToken.token == token)
        refresh_token = session.exec(statement).first()

        if refresh_token:
            refresh_token.is_active = False
            session.add(refresh_token)
            session.commit()
            return True

        return False

    @staticmethod
    def revoke_all_user_refresh_tokens(session: Session, user_id: int) -> int:
        """
        Revoke all refresh tokens for a specific user.

        Args:
            session: Database session
            user_id: ID of the user whose tokens to revoke

        Returns:
            Number of tokens revoked
        """
        statement = select(RefreshToken).where(RefreshToken.user_id == user_id)
        tokens = session.exec(statement).all()

        revoked_count = 0
        for token in tokens:
            token.is_active = False
            session.add(token)
            revoked_count += 1

        session.commit()
        return revoked_count

    @staticmethod
    def cleanup_expired_tokens(session: Session) -> int:
        """
        Remove all expired refresh tokens from the database.

        Args:
            session: Database session

        Returns:
            Number of tokens cleaned up
        """
        statement = select(RefreshToken).where(RefreshToken.expires_at < datetime.utcnow())
        expired_tokens = session.exec(statement).all()

        cleaned_count = 0
        for token in expired_tokens:
            session.delete(token)
            cleaned_count += 1

        session.commit()
        return cleaned_count