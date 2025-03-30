import uuid
import json
import os


from json_handler import JSONHandler
from global_state import DEBUG

from errors import Error, DocumentNotFoundError

class SimpleDocumentDB:
    def __init__(self, db_path="mydb"):
        self.db_path = db_path
        os.makedirs(self.db_path, exist_ok=True)
        self.ids = []
        self.ids_collection = {}

    def get_path_by_id(self, id):
        
        self.update_ids_map()
        
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

    def insert_one(self, collection, document):
        return JSONHandler.parse_data(document, source_db=self, collection_name=collection)

    def find(self, collection, query=None):

        self.update_ids_map()
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

        self.update_ids_map()

        if id not in self.ids:
            raise DocumentNotFoundError(f"Document {id} not found")
            # or return None

        target_path = self.get_path_by_id(id)

        return self.get_document_by_path(target_path)

    def get_document_by_path(self, path):
        return JSONHandler.read_json_file(path)

    def update_ids_map(self):
        
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
        self.update_ids_map()

        if id not in self.ids:
            print(f"Document {id} not found")
            raise DocumentNotFoundError(f"Document {id} not found")

        target_path = self.get_path_by_id(id)
        os.remove(target_path)
        print(f"Document {id} deleted")
        return True


    def init_collection(self, collection_name):

        collection_path = os.path.join(self.db_path, collection_name)
        if os.path.exists(collection_path):
            print(f"Collection {collection_name} already exists")
            return True
        os.mkdir(collection_path)
        return True