import os
from db_utils.utils import get_random_uuid


from json_handler import JSONHandler
from global_state import DEBUG

from errors import Error, DocumentNotFoundError

# TODO: Implement a simple query language for more flexible searches
# TODO: Add support for data export and import (e.g., CSV, JSON)
# TODO: Implement basic analytics functions (e.g., count, sum, average)

class SimpleDocumentDB:
    def __init__(self, db_path="mydb"):
        # TODO: Consider adding a configuration file for default settings
        # TODO: Implement logging instead of print statements for better debugging        
        self.db_path = db_path
        os.makedirs(self.db_path, exist_ok=True)
        self.ids = []
        self.ids_collection = {}
        self.populating_db_state()

    def get_path_by_id(self, id):
                
        if id in self.ids_collection:
            return os.path.join(self.db_path, self.ids_collection[id], f"{id}.json")
        return os.path.join(self.db_path, f"{id}.json")

    def update_document_by_id(self, collection_name, data, id):
        
        document = self.get_document_by_id(id)
        if not document:
            print(f"Document {id} not found")
            raise DocumentNotFoundError(f"Document {id} not found")

        target_path = self.get_path_by_id(id)

        JSONHandler.write_json_file(target_path, data)
        print(f"Document {id} updated")

    def _defaut_data(self, file_name):
        return {
                "message": "This is a JSON file created based on the file name.",
                "file_name": file_name
                }
    
    def insert_one(self, collection_name, data):
        # TODO: Implement data validation (e.g., schema validation)
        # TODO: Add support for auto-incrementing IDs as an alternative to UUIDs
        file_name = get_random_uuid()

        source_db_path = self.db_path
        target_path = os.path.join(source_db_path, collection_name) if collection_name is not None else f"{source_db_path}"
        storage_path = os.path.join(target_path, f"{file_name}.json")

        self.init_collection(collection_name)

        data = self._defaut_data(file_name) if not data else data

        if not JSONHandler.is_json_compatible(data):
            raise Error(f"Data is not JSON compatible: {data}")        

        JSONHandler.parse_data(data, storage_path)

        id_result = file_name

        if id_result:
            self.ids.append(id_result)
            self.ids_collection[id_result] = collection_name
        return id_result

    def find(self, collection, query=None):
        # TODO: Implement more advanced querying (e.g., regex, greater than, less than)
        # TODO: Add pagination support for large result sets
        self.populating_db_state()
        results = []
        for id in self.ids:
            document = self.get_document_by_id(id)
            document_dict = self.convert_to_dict(document)
            if document:
                if query:
                    for key, value in query.items():
                        if key in document and document[key] == value:
                            results.append({id: document})
                else:
                    results.append({id: document})

        return results

    def convert_to_dict(self, document):
        if isinstance(document, dict):
            return document
        return dict(document)

    def get_document_by_id(self, id):

        print(f"[DEBUG] id = {id}") if DEBUG else None
        print(f"[DEBUG] ids = {self.ids}") if DEBUG else None
        if id not in self.ids:
            raise DocumentNotFoundError(f"Document {id} not found")

        target_path = self.get_path_by_id(id)

        return self.get_document_by_path(target_path)

    def get_document_by_path(self, path):
        return JSONHandler.read_json_file(path)

    def populating_db_state(self):
        
        ids = []
        ids_collection = {}
        for dirpath, dirnames, filenames in os.walk(self.db_path):
            for filename in filenames:
                id = filename.replace(".json","")
                ids.append(id)
                ids_collection[id] = os.path.basename(dirpath)

        self.ids = ids
        self.ids_collection = ids_collection

    def update_one(self, collection, query, update_fields):
        ...

    def delete_document_by_id(self, id):
        # TODO: Implement soft delete option (mark as deleted instead of removing)
        # TODO: Add bulk delete functionality
        if id not in self.ids:
            print(f"Document {id} not found")
            raise DocumentNotFoundError(f"Document {id} not found")

        target_path = self.get_path_by_id(id)
        os.remove(target_path)
        print(f"Document {id} deleted")

        self.ids.remove(id)
        del self.ids_collection[id]

        return True


    def init_collection(self, collection_name):

        collection_path = os.path.join(self.db_path, collection_name)
        if os.path.exists(collection_path):
            print(f"[DEBUG] Collection {collection_name} already exists") if DEBUG else None
            return True
        os.mkdir(collection_path)
        return True