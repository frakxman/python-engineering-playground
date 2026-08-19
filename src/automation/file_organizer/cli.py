import argparse
from pathlib import Path


def parse_arguments():
    """
    Parse command line arguments for the File Organizer.

    Returns:
        argparse.Namespace: Parsed arguments containing path, config, dry_run, and recursive flags.
    """
    parser = argparse.ArgumentParser(
        description="Organize files into categorized folders based on extension rules.",
        epilog="Example: python main.py --path ~/Downloads --dry-run"
    )

    parser.add_argument(
        "--path",
        type=Path,
        required=True,
        help="Target directory to organize (e.g., ~/Downloads)."
    )

    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to a custom rules.json file. If not provided, uses 'rules.json' in the current directory."
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate operations without actually moving any files. Safe preview mode."
    )

    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Process subdirectories recursively. If not set, only scans the top-level folder."
    )

    return parser.parse_args()