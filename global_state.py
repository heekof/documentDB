from db_utils.utils import read_json_file
import os

# Determine the config path (can use environment variables)
CONFIG_PATH = os.getenv("APP_SETTINGS_PATH", "settings.json")

class Settings:
    # --- Class-level initialization ---
    _config_path = CONFIG_PATH
    _settings_data = {} # Default to empty

    try:
        # Read the settings immediately when the class is defined
        _settings_data = read_json_file(_config_path)
    except Exception as e:
        # Handle potential errors during initial load if needed,
        # though read_json_file should handle basic ones.
        print(f"Critical error during Settings class definition: {e}")

    # --- Define class attributes based on loaded data ---
    # Use .get() with defaults for robustness
    DEBUG = _settings_data.get("debug", False) # Default to False if 'debug' not in JSON or file missing
    DATABASE_URL = _settings_data.get("database_url", None)
    SECRET_KEY = _settings_data.get("secret_key", "default-secret")
    # Add other settings you expect here...

    # Optional: Allow getting any setting via a class method
    @classmethod
    def get(cls, key, default=None):
        """Get a setting dynamically, providing a default."""
        return cls._settings_data.get(key, default)

    def __repr__(self):
        return f"{self._settings_data}"

    def __str__(self):
        return f"{self._settings_data}"


if __name__ == "__main__":

    # Now you can access DEBUG directly on the class
    print(f"Settings.DEBUG: {Settings.DEBUG}")
    print(f"Settings.DATABASE_URL: {Settings.DATABASE_URL}")
    print(f"Settings.SECRET_KEY: {Settings.SECRET_KEY}") # Will use default
    print(f"Settings.get('some_other_key', 'default_value'): {Settings.get('some_other_key', 'default_value')}")