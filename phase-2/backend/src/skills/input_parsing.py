"""
Input parsing skill module.

This module handles normalization and conversion of raw user input following the reusable skills architecture.
"""

from typing import Any, Dict, Optional
from datetime import datetime


def parse_task_input(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and normalize task input data.

    Args:
        raw_data: Raw input data from user

    Returns:
        Dictionary with normalized task data
    """
    parsed_data = {}

    # Parse and normalize title
    if 'title' in raw_data:
        title = raw_data['title']
        if isinstance(title, str):
            parsed_data['title'] = title.strip()
        else:
            parsed_data['title'] = str(title).strip()

    # Parse and normalize description
    if 'description' in raw_data:
        description = raw_data['description']
        if description is not None and isinstance(description, str):
            parsed_data['description'] = description.strip()
        elif description is not None:
            parsed_data['description'] = str(description).strip()
        else:
            parsed_data['description'] = None

    # Parse and normalize completion status
    if 'is_completed' in raw_data:
        is_completed = raw_data['is_completed']
        if isinstance(is_completed, bool):
            parsed_data['is_completed'] = is_completed
        elif isinstance(is_completed, str):
            parsed_data['is_completed'] = is_completed.lower() in ('true', '1', 'yes', 'on')
        elif isinstance(is_completed, int):
            parsed_data['is_completed'] = bool(is_completed)
        else:
            parsed_data['is_completed'] = False
    else:
        parsed_data['is_completed'] = False

    # Parse and normalize due date
    if 'due_date' in raw_data:
        due_date = raw_data['due_date']
        if due_date is not None:
            if isinstance(due_date, str):
                try:
                    parsed_data['due_date'] = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                except ValueError:
                    try:
                        parsed_data['due_date'] = datetime.strptime(due_date, '%Y-%m-%d')
                    except ValueError:
                        parsed_data['due_date'] = None
            elif isinstance(due_date, datetime):
                parsed_data['due_date'] = due_date
            else:
                parsed_data['due_date'] = None
        else:
            parsed_data['due_date'] = None

    # Parse and normalize status
    if 'status' in raw_data:
        status = raw_data['status']
        if isinstance(status, str):
            status_lower = status.lower()
            if status_lower in ['todo', 'in-progress', 'review', 'done']:
                parsed_data['status'] = status_lower
            else:
                parsed_data['status'] = 'todo'
        else:
            parsed_data['status'] = 'todo'

    # Parse and normalize priority
    if 'priority' in raw_data:
        priority = raw_data['priority']
        if isinstance(priority, str):
            priority_lower = priority.lower()
            if priority_lower in ['low', 'medium', 'high', 'urgent']:
                parsed_data['priority'] = priority_lower
            else:
                parsed_data['priority'] = 'medium'
        else:
            parsed_data['priority'] = 'medium'

    # Parse and normalize category
    if 'category' in raw_data:
        category = raw_data['category']
        if category is not None and isinstance(category, str):
            parsed_data['category'] = category.strip()
        else:
            parsed_data['category'] = None

    # Parse and normalize tags
    if 'tags' in raw_data:
        tags = raw_data['tags']
        if tags is not None:
            if isinstance(tags, list):
                # Convert list to comma-separated string
                parsed_data['tags'] = ','.join([str(tag).strip() for tag in tags if str(tag).strip()])
            elif isinstance(tags, str):
                # Ensure tags are comma-separated
                parsed_data['tags'] = tags.strip()
            else:
                parsed_data['tags'] = str(tags).strip() if str(tags).strip() else None
        else:
            parsed_data['tags'] = None

    return parsed_data


def parse_user_input(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and normalize user input data.

    Args:
        raw_data: Raw input data from user

    Returns:
        Dictionary with normalized user data
    """
    parsed_data = {}

    # Parse and normalize email
    if 'email' in raw_data:
        email = raw_data['email']
        if isinstance(email, str):
            parsed_data['email'] = email.strip().lower()
        else:
            parsed_data['email'] = str(email).strip().lower()

    # Parse and normalize password
    if 'password' in raw_data:
        password = raw_data['password']
        if isinstance(password, str):
            parsed_data['password'] = password.strip()
        else:
            parsed_data['password'] = str(password).strip()

    return parsed_data


def parse_query_params(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and normalize query parameters.

    Args:
        params: Raw query parameters

    Returns:
        Dictionary with normalized query parameters
    """
    parsed_params = {}

    # Parse limit parameter
    if 'limit' in params:
        try:
            limit = int(params['limit'])
            parsed_params['limit'] = max(1, min(limit, 100))  # Clamp between 1 and 100
        except (ValueError, TypeError):
            parsed_params['limit'] = 50

    # Parse offset parameter
    if 'offset' in params:
        try:
            offset = int(params['offset'])
            parsed_params['offset'] = max(0, offset)
        except (ValueError, TypeError):
            parsed_params['offset'] = 0

    # Parse status parameter
    if 'status' in params:
        status = params['status']
        if isinstance(status, str):
            status_lower = status.lower()
            if status_lower in ['all', 'pending', 'completed']:
                parsed_params['status'] = status_lower
            else:
                parsed_params['status'] = 'all'
        else:
            parsed_params['status'] = 'all'
    else:
        parsed_params['status'] = 'all'

    return parsed_params


def parse_auth_token_header(auth_header: Optional[str]) -> Optional[str]:
    """
    Parse and extract JWT token from Authorization header.

    Args:
        auth_header: Authorization header value

    Returns:
        JWT token string or None if invalid format
    """
    if not auth_header:
        return None

    if not isinstance(auth_header, str):
        return None

    # Expected format: "Bearer <token>"
    parts = auth_header.split(' ')
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return None

    return parts[1]


def normalize_whitespace(text: Optional[str]) -> Optional[str]:
    """
    Normalize whitespace in text by trimming and collapsing multiple spaces.

    Args:
        text: Input text

    Returns:
        Normalized text
    """
    if text is None:
        return None

    return ' '.join(text.split())