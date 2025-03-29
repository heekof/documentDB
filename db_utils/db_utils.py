import uuid
import json
import os

def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def get_random_uuid():
    return str(uuid.uuid4())


def create_json_file_based_on_name(data, source_db, collection_name=None):
    
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
    
    with open(storage_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
        