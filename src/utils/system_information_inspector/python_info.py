"""Running Python interpreter version."""
import platform
import sys


def get_python_version() -> str:
    """Return the running Python interpreter's version.
 
    `platform.python_version()` gives a simple string (e.g. "3.12.3"),
    while `sys.version_info` is a named tuple with major/minor/micro
    detail, useful for programmatic comparisons like
    `if sys.version_info >= (3, 10)`.
 
    Returns:
        str: Formatted as "<version> (<version_info tuple>)".
    """

    version = platform.python_version()

    details = sys.version_info

    return f"{version} ({details})"