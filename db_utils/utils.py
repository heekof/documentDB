import uuid
import json
from functools import lru_cache # Optional: for caching file read


def get_random_uuid() -> str:
    return str(uuid.uuid4())


@lru_cache(maxsize=1) # Cache the result of reading the file
def read_json_file(file_path):
    """Reads a JSON file and returns its content."""
    print(f"Reading settings from: {file_path}") # Add print for clarity
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: Configuration file '{file_path}' not found.")
        return {} # Return empty dict if file not found
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{file_path}'.")
        return {} # Return empty dict on decode error
    except Exception as e:
        print(f"An unexpected error occurred reading '{file_path}': {e}")
        return {}