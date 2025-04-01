import json
import os
import json

from global_state import DEBUG

from errors import Error

class JSONHandler:

    def __init__(self):
        pass

    @staticmethod
    def is_valid_json(data: str) -> bool:
        try:
            json.loads(data)
            return True
        except (Error):
            raise Error(f"Expected a json, got {type(data)}")
            return False

    @staticmethod
    def is_json_compatible(data) -> bool:
        if not isinstance(data, dict):
            raise Error(f"insert_one() expects a dict, got {type(data)}")
        
        if isinstance(data, (dict, list)):
            return True
        if isinstance(data, str):
            try:
                json.loads(data)
                return True
            except json.JSONDecodeError:
                return False
        raise Error(f"Expected str, dict, or list. Got: {type(data).__name__}")

    @staticmethod
    def read_json_file(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)

        print(f"[DEBUG] Raw loaded data: {data} (type: {type(data).__name__}) path: {file_path}") if DEBUG else None

        if not isinstance(data, dict):
            raise Error(f"Expected JSON object (dict), got {type(data).__name__}")
        return data

    @staticmethod
    def write_json_file(file_path, data):
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def parse_data(data, storage_path):        
        JSONHandler.write_json_file(storage_path, data)
        