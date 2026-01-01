"""
Shared utilities for Todo CLI application
Provides common helper functions
"""

from datetime import datetime
from typing import Optional


def get_current_timestamp() -> str:
    """
    Generate current timestamp in ISO 8601 format.

    Returns:
        Timestamp string in format YYYY-MM-DDTHH:MM:SSZ
    """
    return datetime.utcnow().isoformat(timespec='seconds') + "Z"


def normalize_text(text: str) -> str:
    """
    Normalize text by trimming and collapsing spaces.

    Args:
        text: Raw text to normalize

    Returns:
        Normalized text string
    """
    # Trim leading/trailing whitespace
    normalized = text.strip()

    # Collapse multiple spaces into single space
    words = normalized.split()
    collapsed = " ".join(words)

    return collapsed


def truncate_string(text: str, max_length: int) -> str:
    """
    Truncate string to maximum length with ellipsis.

    Args:
        text: String to truncate
        max_length: Maximum allowed length

    Returns:
        Truncated string with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def format_duration(start_time: datetime, end_time: datetime) -> str:
    """
    Format duration between two timestamps.

    Args:
        start_time: Start timestamp
        end_time: End timestamp

    Returns:
        Formatted duration string
    """
    duration = end_time - start_time
    total_seconds = int(duration.total_seconds())

    if total_seconds < 60:
        return f"{total_seconds}s"
    elif total_seconds < 3600:
        minutes = total_seconds // 60
        return f"{minutes}m"
    else:
        hours = total_seconds // 3600
        return f"{hours}h"
