import uuid
import json
import os

# TODO : check if file exist before creation
# TODO : manage collections creation etc



class SimpleDocumentDB:
    def __init__(self, db_path="mydb"):
        ...

    def create_collection(self, name):
        ...

    def insert_one(self, collection, document):
        """
        if collection in collections, check document and then add it. otherwise create it.


        """
        ...

    def find(self, collection, query=None):
        ...

    def update_one(self, collection, query, update_fields):
        ...

    def delete_one(self, collection, query):
        ...

db = SimpleDocumentDB()

db.insert_one("users", {"name": "Jaafar", "age": 34})
results = db.find("users", {"age": 34})




def get_random_uuid():
    return str(uuid.uuid4())

random_uuid = get_random_uuid()
print(random_uuid)



def create_json_file_based_on_name(file_name, source_db='mydb', collection_name=None):
    
    if collection:
        storage_path = f"{source_db}/{collection_name}/{file_name}.json"
    else:
        storage_path = f"{source_db}/{file_name}.json"

    data = {
        "message": "This is a JSON file created based on the file name.",
        "file_name": file_name
        }
    
    with open(storage_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)



create_json_file_based_on_name(random_uuid)
