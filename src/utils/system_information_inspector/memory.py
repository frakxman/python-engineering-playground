"""Physical RAM detection, implemented per-OS with the standard library only.

There is no single stdlib function that reports total RAM across
platforms (that's what third-party libraries like `psutil` are for).
This module branches by OS instead:

- Linux / macOS: uses `os.sysconf()` to read page size and physical
  page count directly from the kernel.
- Windows: uses `ctypes` to call the Win32 API function
  `GlobalMemoryStatusEx` directly, since `os.sysconf()` doesn't exist
  on Windows.
"""

import ctypes
import os
import platform


def get_memory() -> str:
    """Return total physical RAM, formatted in gigabytes.

    Returns:
        str: Memory formatted as "<value> GB", "Not available" if the
        OS isn't supported, or an error message if reading memory
        failed unexpectedly.
    """
    system = platform.system()

    try:

        if system in ("Linux", "Darwin"):

            page_size = os.sysconf("SC_PAGE_SIZE")
            total_pages = os.sysconf("SC_PHYS_PAGES")

            total_bytes = page_size * total_pages
            total_gb = total_bytes / (1024 ** 3)

            return f"{total_gb:.2f} GB"

        elif system == "Windows":

            class MEMORYSTATUSEX(ctypes.Structure):
                """Mirrors the Win32 MEMORYSTATUSEX C struct field-for-field,
                so ctypes can fill it via GlobalMemoryStatusEx."""

                _fields_ = [

                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]

            memory = MEMORYSTATUSEX()

            memory.dwLength = ctypes.sizeof(MEMORYSTATUSEX)

            ctypes.windll.kernel32.GlobalMemoryStatusEx(
                ctypes.byref(memory)
            )

            total_gb = memory.ullTotalPhys / (1024 ** 3)

            return f"{total_gb:.2f} GB"

        return "Not available"

    except Exception as e:
        # Keep the OS branch that failed in the message — a bare
        # str(e) alone doesn't say *where* it happened.
        return f"Memory not available ({e})"