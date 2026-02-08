"""
Input parsing skill for Todo CLI application
Normalizes and converts raw user input into clean, usable data
"""

from typing import Optional, Dict, Any


def parse_menu_selection(user_input: str, max_option: int) -> Dict[str, Any]:
    """
    Parse menu selection into valid integer.

    Args:
        user_input: Raw user input string
        max_option: Maximum valid menu option number

    Returns:
        Dictionary with:
            - valid (bool): True if parsing succeeds
            - error (str): Error message if parsing fails
            - value (int): Parsed integer value
    """
    normalized = user_input.strip()

    # Empty input
    if normalized == "":
        return {
            "valid": False,
            "error": "Selection cannot be empty. Please enter a valid option number.",
            "value": None
        }

    # Try to parse as integer
    try:
        value = int(normalized)
    except ValueError:
        return {
            "valid": False,
            "error": f"Invalid selection: '{normalized}'. Expected a number (1-{max_option}).",
            "value": None
        }

    # Validate range
    if value < 1 or value > max_option:
        return {
            "valid": False,
            "error": f"Invalid selection: {value}. Please choose between 1 and {max_option}.",
            "value": None
        }

    return {
        "valid": True,
        "error": None,
        "value": value
    }


def parse_task_id(user_input: str) -> Dict[str, Any]:
    """
    Parse task ID from user input.

    Args:
        user_input: Raw user input string

    Returns:
        Dictionary with:
            - valid (bool): True if parsing succeeds
            - error (str): Error message if parsing fails
            - value (int): Parsed task ID
    """
    normalized = user_input.strip()

    # Empty input
    if normalized == "":
        return {
            "valid": False,
            "error": "Task ID cannot be empty. Please provide a valid task ID.",
            "value": None
        }

    # Try to parse as integer
    try:
        value = int(normalized)
    except ValueError:
        return {
            "valid": False,
            "error": f"Invalid task ID: '{normalized}'. Expected a number (e.g., 1, 2, 3).",
            "value": None
        }

    # Validate ID is positive
    if value <= 0:
        return {
            "valid": False,
            "error": f"Invalid task ID: {value}. Task IDs must be positive numbers (1, 2, 3, ...).",
            "value": None
        }

    return {
        "valid": True,
        "error": None,
        "value": value
    }


def parse_text_input(user_input: str) -> Dict[str, Any]:
    """
    Parse and normalize text input (title, description).

    Args:
        user_input: Raw user input string

    Returns:
        Dictionary with:
            - valid (bool): True if parsing succeeds
            - error (str): Error message if parsing fails
            - value (str): Normalized text
    """
    normalized = user_input.strip()

    # Empty input
    if normalized == "":
        return {
            "valid": False,
            "error": "Input cannot be empty. Please provide a valid text.",
            "value": None
        }

    # Collapse multiple spaces into single space
    words = normalized.split()
    collapsed = " ".join(words)

    return {
        "valid": True,
        "error": None,
        "value": collapsed
    }


def parse_boolean_input(user_input: str) -> Dict[str, Any]:
    """
    Parse boolean input (yes/no, y/n, true/false).

    Args:
        user_input: Raw user input string

    Returns:
        Dictionary with:
            - valid (bool): True if parsing succeeds
            - error (str): Error message if parsing fails
            - value (bool): Parsed boolean value
    """
    normalized = user_input.strip().lower()

    # Yes variations
    yes_variations = ["y", "yes", "true", "1"]
    # No variations
    no_variations = ["n", "no", "false", "0"]

    if normalized in yes_variations:
        return {
            "valid": True,
            "error": None,
            "value": True
        }

    if normalized in no_variations:
        return {
            "valid": True,
            "error": None,
            "value": False
        }

    return {
        "valid": False,
        "error": f"Invalid input: '{normalized}'. Expected yes/no, y/n, true/false, or 1/0.",
        "value": None
    }
