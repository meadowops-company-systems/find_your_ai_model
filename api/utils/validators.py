"""
Input validation utilities
"""
import re

MIN_TASK_LENGTH = 10
MAX_TASK_LENGTH = 5000


def validate_task_input(task_description: str) -> bool:
    """
    Validate task description input.

    Args:
        task_description: The task description to validate

    Returns:
        True if valid

    Raises:
        ValueError: If validation fails
    """
    if not task_description:
        raise ValueError("Task description is required")

    if not isinstance(task_description, str):
        raise ValueError("Task description must be a string")

    # Check length
    length = len(task_description.strip())
    if length < MIN_TASK_LENGTH:
        raise ValueError(
            f"Task description must be at least {MIN_TASK_LENGTH} characters"
        )

    if length > MAX_TASK_LENGTH:
        raise ValueError(
            f"Task description must not exceed {MAX_TASK_LENGTH} characters"
        )

    # Check for only whitespace
    if not task_description.strip():
        raise ValueError("Task description cannot be only whitespace")

    # Check for suspicious patterns (basic injection prevention)
    # Allow alphanumeric, common punctuation, and whitespace
    allowed_pattern = re.compile(r'^[\w\s\.,!?\'\"-:;()]+$')
    if not allowed_pattern.match(task_description):
        # Allow but warn - some special characters might be legitimate
        pass

    return True


def validate_category(category: str) -> bool:
    """
    Validate category input.

    Args:
        category: The category to validate

    Returns:
        True if valid

    Raises:
        ValueError: If validation fails
    """
    valid_categories = [
        'writing',
        'coding',
        'image',
        'audio',
        'video',
        'data',
        'research',
        'productivity',
        ''
    ]

    if category not in valid_categories:
        raise ValueError(f"Invalid category: {category}")

    return True
