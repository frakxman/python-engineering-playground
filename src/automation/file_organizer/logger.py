import logging
from pathlib import Path
from datetime import datetime

# Global variable to keep track of whether the logger has been configured
_logger_configured = False


def setup_logger(name: str = "FileOrganizer", log_file: Path = Path("file_organizer.log")) -> logging.Logger:
    """
    Configure and return a logger with both console and file handlers.

    This function ensures that logs are displayed in the terminal with a clean format
    and also persisted to a log file with full timestamp details for auditing.

    Args:
        name: The name of the logger (usually the module name).
        log_file: Path object pointing to the log file location.

    Returns:
        Configured Logger instance.
    """
    global _logger_configured

    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers if this function is called multiple times
    if _logger_configured:
        return logger

    # Set the base logging level (captures all levels DEBUG and above)
    logger.setLevel(logging.DEBUG)

    # ----- Console Handler (for the terminal) -----
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Show only INFO and above in console
    console_format = logging.Formatter(
        '%(levelname)s: %(message)s'  # Simple format: "ERROR: Something went wrong"
    )
    console_handler.setFormatter(console_format)

    # ----- File Handler (for persistent storage) -----
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)  # Save everything, from DEBUG to CRITICAL
    file_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'  # ISO-like date format
    )
    file_handler.setFormatter(file_format)

    # Add both handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    _logger_configured = True
    return logger


def get_logger(name: str = "FileOrganizer") -> logging.Logger:
    """
    Get the configured logger instance.

    If the logger hasn't been set up yet, it initializes it with default settings.
    This is a convenience wrapper around setup_logger().
    """
    return setup_logger(name)


# --- Self-test block ---
if __name__ == "__main__":
    # Test the logger with a temporary log file
    test_log_path = Path("test_organizer.log")

    print("🧪 Testing logger setup...")
    logger = setup_logger("TestLogger", test_log_path)

    # Log messages at different levels
    logger.debug("This is a DEBUG message (only visible in the log file).")
    logger.info("This is an INFO message (visible in console and file).")
    logger.warning("This is a WARNING message.")
    logger.error("This is an ERROR message.")
    logger.critical("This is a CRITICAL message.")

    # Verify the log file was created
    if test_log_path.exists():
        print(f"\n✅ Log file created successfully: {test_log_path}")
        print("\n📄 Contents of the log file:")
        print("-" * 40)
        with open(test_log_path, 'r', encoding='utf-8') as f:
            print(f.read().strip())
        print("-" * 40)

        # Close and remove all handlers to release the file
        logger.handlers.clear()
        logging.shutdown()

        # Clean up the test file
        try:
            test_log_path.unlink()
            print("\n🧹 Test log file cleaned up.")
        except PermissionError as e:
            print(f"\n⚠️ Could not delete the file (maybe it's still open): {e}")
            print("You can manually delete 'test_organizer.log' later.")
    else:
        print("\n❌ Error: Log file was not created.")