"""Current local date and time."""
from datetime import datetime


def get_current_datetime() -> str:
    """Return the current local date and time.
 
    Returns:
        str: Formatted as "YYYY-MM-DD HH:MM:SS".
    """

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")