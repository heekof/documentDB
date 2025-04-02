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


def get_all_values_from_dict(dictionary : dict) -> list:
    values = []
    if isinstance(dictionary, dict):
        for v in dictionary.values():
            values.extend(get_all_values_from_dict(v))
    elif isinstance(dictionary, list):
        for item in dictionary:
            values.extend(get_all_values_from_dict(item))
    else:
        values.append(dictionary)
    return values


def walkthrough_dict(dictionary: dict):
    for key, value in dictionary.items():
        if isinstance(value, dict):
            walkthrough_dict(value)
        else:
            print(f"Key: {key}, Value: {value}")


def walkthrough_dict_apply_function(dictionary: dict, func : callable):
    for key, value in dictionary.items():
        if isinstance(value, dict):
            walkthrough_dict_apply_function(value, func)
        else:
            func(key, value)


if __name__ == "__main__":
    dictionary = { "key1": "value1", "key2": { "key3": "value3", "key4": "value4", "key5": "".join(["v1","v2","v3"]) } }

    print(
        walkthrough_dict_apply_function(dictionary, lambda key, value: print(key+"_"+value) ) )
        