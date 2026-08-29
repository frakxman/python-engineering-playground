"""CPU model detection, with a Linux-specific fallback.

`platform.processor()` returns an empty string on many Linux systems
because Linux doesn't expose the CPU model through that API by
default. When that happens, this module falls back to reading
`/proc/cpuinfo` directly.
"""

import platform


def get_processor() -> str:
    """Return the processor (CPU) model name.

    Tries `platform.processor()` first. If it comes back empty and
    the OS is Linux, reads `/proc/cpuinfo` and extracts the
    "model name" field as a fallback.

    Returns:
        str: The processor model name, or "Not available" if it
        could not be determined on this platform.
    """
    processor = platform.processor()

    if not processor and platform.system() == "Linux":
        try:
            with open("/proc/cpuinfo", "r") as cpuinfo:

                for line in cpuinfo:

                    if line.startswith("model name"):

                        processor = line.split(":", 1)[1].strip()
                        break

        except FileNotFoundError:
            pass

    return processor if processor else "Not available"