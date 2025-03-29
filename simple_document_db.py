import uuid
import json
import os


from json_handler import JSONHandler

class SimpleDocumentDB:
    def __init__(self, db_path="mydb"):
        self.db_path = db_path

        self.ids = []
        self.ids_collection = {}

    def create_collection(self, name):
        ...

    def insert_one(self, collection, document):
        return JSONHandler.parse_data(document, source_db=self, collection_name=collection)

    # db.find("users", {"age": 34})
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
                            results.append(document)
                else:
                    results.append(document)

        return results

    def convert_to_dict(self, document):
        if isinstance(document, dict):
            return document
        return dict(document)

    def get_document_by_id(self, id):

        self.update_ids_map()

        if id not in self.ids:
            return False

        if self.ids_collection[id]:
            target_path = os.path.join(self.db_path, self.ids_collection[id], f"{id}.json")
        else:
            target_path = os.path.join(self.db_path, f"{id}.json")

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
                ids_collection[id] = dirpath.split("/")[-1]

        self.ids = ids
        self.ids_collection = ids_collection

    def update_one(self, collection, query, update_fields):
        ...

    def delete_one(self, collection, query):
        ...

    def init_collection(self, collection_name):
        collection_path = f"{self.db_path}/{collection_name}"

        if os.path.exists(collection_path) or not collection_name:
            return False
        
        print(collection_path)
        os.mkdir(collection_path)
        return True