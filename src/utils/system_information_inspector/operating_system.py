"""Operating system identity: name, version, and architecture.

Wraps the parts of the standard `platform` module that describe
*which* OS is running and *what* build/architecture it is, so callers
never need to touch `platform` directly.
"""

import platform


def get_operating_system() -> str:
    """Return the operating system name.

    Returns:
        str: Short OS name as reported by the interpreter,
        e.g. "Linux", "Windows", or "Darwin" (macOS).
    """
    return platform.system()


def get_os_version() -> str:
    """Return the operating system version.

    Combines `platform.release()` (human-readable version, e.g. "10"
    on Windows) with `platform.version()` (internal kernel/build
    string) since each answers a different question.

    Returns:
        str: Version string formatted as "<release> (build: <version>)".
    """
    return f"{platform.release()} (build: {platform.version()})"


def get_architecture() -> str:
    """Return interpreter and machine architecture information.

    `platform.architecture()` describes the running Python binary
    (32-bit vs 64-bit), while `platform.machine()` describes the
    physical CPU architecture (e.g. "x86_64", "arm64"). Both are
    reported because a 32-bit Python can run on 64-bit hardware.

    Returns:
        str: Formatted as "<bits> (<executable format>) - Machine: <machine>".
    """
    bits, executable = platform.architecture()
    machine = platform.machine()

    return f"{bits} ({executable}) - Machine: {machine}"