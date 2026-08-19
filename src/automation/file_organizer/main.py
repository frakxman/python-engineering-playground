import sys
from pathlib import Path

# Import our own modules
from logger import setup_logger
from config_loader import load_rules, ConfigError
from scanner import FileScanner
from organizer import Organizer
from cli import parse_arguments


def main():
    """
    Main entry point for the File Organizer application.
    Orchestrates the entire flow: CLI parsing, logging setup, config loading,
    scanning, and organization.
    """
    # 1. Parse command line arguments
    args = parse_arguments()

    # 2. Setup logging (console + file)
    logger = setup_logger("FileOrganizer", Path("file_organizer.log"))
    logger.info("=" * 60)
    logger.info("🚀 File Organizer started")
    logger.info(f"Target path: {args.path}")
    logger.info(f"Dry-run mode: {args.dry_run}")
    logger.info(f"Recursive mode: {args.recursive}")

    # 3. Determine configuration file path
    if args.config:
        config_path = args.config
    else:
        # Default: look for rules.json in the same directory as this script (main.py)
        config_path = Path(__file__).parent / "rules.json"

    # 4. Validate target directory
    if not args.path.exists():
        logger.error(f"❌ Target directory not found: {args.path}")
        sys.exit(1)

    if not args.path.is_dir():
        logger.error(f"❌ Path is not a directory: {args.path}")
        sys.exit(1)

    # 5. Load sorting rules
    try:
        logger.info(f"📄 Loading rules from: {config_path}")
        rules = load_rules(config_path)
        logger.info(f"✅ Loaded {len(rules)} categories.")
    except ConfigError as e:
        logger.error(f"❌ Configuration error: {e}")
        sys.exit(1)

    # 6. Scan the directory and classify files
    try:
        scanner = FileScanner(rules, recursive=args.recursive)
        logger.info(f"🔍 Scanning directory: {args.path}")
        classified_files = scanner.scan(args.path)

        total_files = sum(len(files) for files in classified_files.values())
        logger.info(f"📊 Found {total_files} files to organize.")

        if total_files == 0:
            logger.info("✨ No files to organize. Exiting.")
            sys.exit(0)

    except FileNotFoundError as e:
        logger.error(f"❌ Scanning error: {e}")
        sys.exit(1)
    except NotADirectoryError as e:
        logger.error(f"❌ Scanning error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Unexpected scanning error: {e}")
        sys.exit(1)

    # 7. Organize the files (move them or dry-run)
    try:
        organizer = Organizer(args.path, dry_run=args.dry_run)
        organizer.organize(classified_files)

        # Log final summary
        if args.dry_run:
            logger.info(f"✅ DRY-RUN completed. Would move {organizer.stats['moved']} files, errors: {organizer.stats['errors']}.")
        else:
            logger.info(f"✅ Organization completed. Moved {organizer.stats['moved']} files, skipped {organizer.stats['skipped']}, errors: {organizer.stats['errors']}.")

    except Exception as e:
        logger.error(f"❌ Organization error: {e}")
        sys.exit(1)

    logger.info("🏁 File Organizer finished successfully.")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()