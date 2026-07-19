"""
Logging configuration utilities
"""
import os
import logging
import sys


def setup_logger(name: str) -> logging.Logger:
    """
    Set up a logger with consistent configuration.

    Args:
        name: Logger name (usually __name__)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)

    # Only configure if not already configured
    if not logger.handlers:
        level = os.getenv('LOG_LEVEL', 'INFO')
        logger.setLevel(getattr(logging, level.upper()))

        # Console handler
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(getattr(logging, level.upper()))

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger


def log_event(logger: logging.Logger, event: str, **fields) -> None:
    """Log a structured event without sensitive payloads."""
    payload = ', '.join(f'{key}={value}' for key, value in fields.items())
    logger.info('%s | %s', event, payload)


# Default logger
logger = setup_logger(__name__)
