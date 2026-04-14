"""
PURPOSE:
Utility helpers for consistent formatting
"""

from datetime import datetime, timezone

def get_utc_timestamp():
    """
    PROMISES:
        returns current UTC timestamp in ISO 8601 format
    """

    return datetime.now(timezone.utc).isoformat()

