import uuid
import json
import os

from db_utils import db_utils as util

class SimpleDocumentDB:
    def __init__(self, db_path="mydb"):
        self.db_path = db_path

        self.ids = []
        self.ids_collection = {}

    def create_collection(self, name):
        ...

    def insert_one(self, collection, document):
        """
        if collection in collections, check document and then add it. otherwise create it.

        db.insert_one("users", {"name": "Jaafar", "age": 34})

        """
        util.create_json_file_based_on_name(document, source_db=self, collection_name=collection)

    def find(self, collection, query=None):
        ...

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
        return util.read_json_file(path)

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