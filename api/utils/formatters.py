"""
Response formatting utilities
"""
from typing import Dict, Any


def format_success_response(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format a successful API response.

    Args:
        data: The response data

    Returns:
        Formatted response dictionary
    """
    return {
        'success': True,
        'data': data
    }


def format_error_response(
    error: str,
    message: str,
    status_code: int = 400
) -> Dict[str, Any]:
    """
    Format an error API response.

    Args:
        error: Error type/category
        message: Human-readable error message
        status_code: HTTP status code (for reference)

    Returns:
        Formatted error response
    """
    return {
        'success': False,
        'error': {
            'type': error,
            'message': message
        }
    }


def format_recommendation_response(
    primary: Dict[str, Any],
    alternatives: list,
    processing_time: int
) -> Dict[str, Any]:
    """
    Format a recommendation response.

    Args:
        primary: Primary recommendation
        alternatives: List of alternative recommendations
        processing_time: Processing time in milliseconds

    Returns:
        Formatted recommendation response
    """
    return {
        'primary': primary,
        'alternatives': alternatives,
        'processingTime': processing_time
    }
