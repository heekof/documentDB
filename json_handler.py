import json
import os

import json

from db_utils.utils import get_random_uuid

class JSONHandler:

    def __init__(self):
        pass

    @staticmethod
    def is_valid_json(data: str) -> bool:
        try:
            json.loads(data)
            return True
        except (ValueError, TypeError):
            raise TypeError(f"Expected a json, got {type(data).__name__}")
            return False

    @staticmethod
    def is_json_compatible(data) -> bool:
        if isinstance(data, (dict, list)):  # JSON must be object or array at the top level
            return True
        if isinstance(data, str):
            try:
                json.loads(data)
                return True
            except ValueError:
                return False
        raise TypeError(f"Expected str, dict, or list. Got: {type(data).__name__}")


    @staticmethod
    def read_json_file(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data

    @staticmethod
    def write_json_file(file_path, data):
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def parse_data(data, source_db, collection_name=None):
        
        file_name = get_random_uuid()

        source_db_path = source_db.db_path
        target_path = f"{source_db_path}/{collection_name}" if collection_name is not None else f"{source_db_path}"
        storage_path = f"{target_path}/{file_name}.json"

        source_db.init_collection(collection_name)

        if not data:
            data = {
                "message": "This is a JSON file created based on the file name.",
                "file_name": file_name
                }

        if not JSONHandler.is_json_compatible(data):
            return False
        
        JSONHandler.write_json_file(storage_path, data)
        return True
        