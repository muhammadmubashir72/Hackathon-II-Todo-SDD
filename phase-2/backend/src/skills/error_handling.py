"""
Error handling skill module.

This module standardizes error generation and display following the reusable skills architecture.
"""

from enum import Enum
from typing import Optional, Dict, Any
from datetime import datetime
from fastapi import HTTPException
from sqlmodel import Session


class ErrorCode(Enum):
    """Enumeration of error codes."""
    INTERNAL_ERROR = "INTERNAL_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    AUTHENTICATION_ERROR = "AUTHENTICATION_ERROR"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    NOT_FOUND = "NOT_FOUND"
    CONFLICT = "CONFLICT"


def create_error_response(
    detail: str,
    error_code: ErrorCode = ErrorCode.INTERNAL_ERROR,
    status_code: int = 500
) -> Dict[str, Any]:
    """
    Create a standardized error response.

    Args:
        detail: Human-readable error message
        error_code: Error code from ErrorCode enum
        status_code: HTTP status code

    Returns:
        Dictionary representing the error response
    """
    return {
        "detail": detail,
        "error_code": error_code.value,
        "timestamp": datetime.utcnow().isoformat(),
        "status_code": status_code
    }


def handle_validation_error(detail: str) -> HTTPException:
    """
    Handle validation errors with standardized response.

    Args:
        detail: Human-readable error message

    Returns:
        HTTPException with 400 status code
    """
    error_response = create_error_response(
        detail=detail,
        error_code=ErrorCode.VALIDATION_ERROR,
        status_code=400
    )
    return HTTPException(
        status_code=400,
        detail=error_response
    )


def handle_authentication_error(detail: str) -> HTTPException:
    """
    Handle authentication errors with standardized response.

    Args:
        detail: Human-readable error message

    Returns:
        HTTPException with 401 status code
    """
    error_response = create_error_response(
        detail=detail,
        error_code=ErrorCode.AUTHENTICATION_ERROR,
        status_code=401
    )
    return HTTPException(
        status_code=401,
        detail=error_response
    )


def handle_permission_denied(detail: str) -> HTTPException:
    """
    Handle permission denied errors with standardized response.

    Args:
        detail: Human-readable error message

    Returns:
        HTTPException with 403 status code
    """
    error_response = create_error_response(
        detail=detail,
        error_code=ErrorCode.PERMISSION_DENIED,
        status_code=403
    )
    return HTTPException(
        status_code=403,
        detail=error_response
    )


def handle_not_found(detail: str) -> HTTPException:
    """
    Handle not found errors with standardized response.

    Args:
        detail: Human-readable error message

    Returns:
        HTTPException with 404 status code
    """
    error_response = create_error_response(
        detail=detail,
        error_code=ErrorCode.NOT_FOUND,
        status_code=404
    )
    return HTTPException(
        status_code=404,
        detail=error_response
    )


def handle_conflict(detail: str) -> HTTPException:
    """
    Handle conflict errors with standardized response.

    Args:
        detail: Human-readable error message

    Returns:
        HTTPException with 409 status code
    """
    error_response = create_error_response(
        detail=detail,
        error_code=ErrorCode.CONFLICT,
        status_code=409
    )
    return HTTPException(
        status_code=409,
        detail=error_response
    )


def log_error(error: Exception, context: Optional[str] = None) -> None:
    """
    Log error with context for debugging purposes.

    Args:
        error: Exception object to log
        context: Additional context information
    """
    import traceback
    import logging

    logger = logging.getLogger(__name__)

    error_msg = f"Error occurred{' in ' + context if context else ''}: {str(error)}"
    logger.error(error_msg)
    logger.error(traceback.format_exc())


def validate_and_handle_db_session(session: Session) -> None:
    """
    Validate database session and handle potential issues.

    Args:
        session: Database session to validate

    Raises:
        HTTPException if session is invalid
    """
    try:
        # Test the session by attempting a simple query
        session.execute("SELECT 1")
    except Exception as e:
        log_error(e, "database session validation")
        raise handle_validation_error("Database session is invalid")


def handle_internal_error(detail: str = "An internal server error occurred") -> HTTPException:
    """
    Handle internal server errors with standardized response.

    Args:
        detail: Human-readable error message

    Returns:
        HTTPException with 500 status code
    """
    error_response = create_error_response(
        detail=detail,
        error_code=ErrorCode.INTERNAL_ERROR,
        status_code=500
    )
    return HTTPException(
        status_code=500,
        detail=error_response
    )