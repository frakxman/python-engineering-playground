import json
from pathlib import Path
from typing import Dict, List

# Custom exception: separates configuration errors from other program errors
class ConfigError(Exception):
    """Custom exception raised when the configuration file is invalid or missing."""
    pass


def load_rules(config_path: Path) -> Dict[str, List[str]]:
    """
    Load and validate sorting rules from a JSON configuration file.

    Args:
        config_path: Path object pointing to the JSON rules file.

    Returns:
        Dictionary where keys are category names and values are lists of extensions (lowercase).

    Raises:
        ConfigError: If the file doesn't exist, contains invalid JSON, or has an invalid structure.
    """
    # Validation 1: Does the file exist?
    if not config_path.exists():
        raise ConfigError(f"Configuration file not found: {config_path}")

    # Validation 2: Is it valid JSON?
    try:
        with open(config_path, 'r', encoding='utf-8') as file:
            raw_data = json.load(file)
    except json.JSONDecodeError as e:
        raise ConfigError(f"Invalid JSON syntax in {config_path}: {e}")

    # Validation 3: Does it have the correct structure?
    processed_data = {}
    for category, extensions in raw_data.items():
        if not isinstance(extensions, list):
            raise ConfigError(
                f"Invalid structure for category '{category}'. Expected list, got {type(extensions).__name__}"
            )
        # Normalize: convert all extensions to lowercase for case-insensitive comparison
        processed_data[category] = [ext.lower() for ext in extensions]

    return processed_data


# --- Self-test block (runs only if this file is executed directly) ---
if __name__ == "__main__":
    try:
        current_dir = Path(__file__).parent
        rules_path = current_dir / "rules.json"
        
        print(f"🔍 Loading rules from: {rules_path}")
        rules = load_rules(rules_path)
        
        print("\n✅ Rules loaded successfully!")
        for category, extensions in rules.items():
            print(f"  📁 {category}: {len(extensions)} extensions")
            
        # Force an error (missing file) to test error handling
        print("\n🧪 Testing error handling (missing file)...")
        fake_path = current_dir / "fake.json"
        load_rules(fake_path)
        
    except ConfigError as e:
        print(f"\n⚠️  Caught expected error: {e}")
        print("✅ Error handling works perfectly!")