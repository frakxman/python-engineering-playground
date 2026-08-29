"""Aggregates every inspection module into a single report.
 
This module only orchestrates calls to the other modules — it holds
no data-gathering logic of its own. That logic lives in
`operating_system.py`, `processor.py`, `memory.py`, `python_info.py`,
and `date_time.py`.
"""
from src.utils.system_information_inspector.operating_system import (
    get_architecture,
    get_operating_system,
    get_os_version,
)

from src.utils.system_information_inspector.processor import get_processor
from src.utils.system_information_inspector.memory import get_memory
from src.utils.system_information_inspector.python_info import get_python_version
from src.utils.system_information_inspector.date_time import get_current_datetime



def build_report() -> dict:
    """Collect results from every inspection module into one report.
 
    Returns:
        dict: Human-readable labels (e.g. "Operating System") mapped
        to their value as a string, ready to print or serialize.
    """

    return {

        "Operating System": get_operating_system(),

        "OS Version": get_os_version(),

        "Architecture": get_architecture(),

        "Processor": get_processor(),

        "Memory": get_memory(),

        "Python": get_python_version(),

        "Current Time": get_current_datetime(),
    }