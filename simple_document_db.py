import os
import json
from db_utils.utils import get_random_uuid

from json_handler import JSONHandler
from global_state import Settings

from errors import Error, DocumentNotFoundError
from document_state import DocumentStatus

DEBUG = Settings.DEBUG

from simple_index import SimpleIndex

from db_utils.utils import get_all_values_from_dict

class SimpleDocumentDB:
    def __init__(self, db_path="mydb", settings: Settings = Settings):
        # TODO: Implement logging instead of print statements for better debugging        
        self.db_path = db_path
        os.makedirs(self.db_path, exist_ok=True)
        self.ids = []
        self.ids_collection = {}
        self.id_status = {}
        self.populating_db_state()
        self.indexes = {}
        self.settings = Settings
        self.document_values_to_index = []
        self.indexing_documents()

        print(f"Database initialized at {self.db_path}")

        print(f"[DEBUG] settings = {self.settings}, type = {type(self.settings)}, port = {self.settings.get('port')}") if DEBUG else None


    def insert_one(self, collection_name, data):

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
            self.id_status[id_result] = DocumentStatus.ACTIVE

            data = self.convert_to_dict(data)
            
            self._index_document(id_result, data)

        return id_result

    def update_document_by_id(self, collection_name, data, id):
        
        document = self.get_document_by_id(id)
        if not document:
            print(f"Document {id} not found")
            raise DocumentNotFoundError(f"Document {id} not found")

        target_path = self.get_path_by_id(id)

        # replace the document with the new data but the data can be partial in the document.
        print(f"[DEBUG] new_data = {data}") if DEBUG else None
        print(f"[DEBUG] document = {document}") if DEBUG else None

        # removing old index for this document
        self._remove_index_for_document(id)

        # indexing document with new data
        self._index_document(id, data)

        for key, value in data.items():
            if key in document:
                document[key] = value
            else:
                document[key] = value

        JSONHandler.parse_data(document, target_path)
        print(f"Document {id} updated")

    def _index_document(self, doc_id, data):
        for key, value in data.items():
            if value not in self.indexes:
                index = SimpleIndex(value)
                index.index_document(doc_id, data)
                self.indexes[value] = index
            else:
                self.indexes[value].index_document(doc_id, data)

    def _defaut_data(self, file_name):
        return {
                "message": "This is a JSON file created based on the file name.",
                "file_name": file_name
                }

    def find(self, collection, query=None):
        self.populating_db_state()
        results = []
        for id in self.ids:
            document = self.get_document_by_id(id)
            document_dict = self.convert_to_dict(document)
            if document:
                if query:
                    print(f"[DEBUG] query = {query}") if DEBUG else None
                    print(f"[DEBUG] document = {document}") if DEBUG else None
                    for key, value in query.items():
                        if key in document and document_dict[key] == value:
                            results.append({id: document_dict})
                else:
                    results.append({id: document})

        return results

    def indexing_documents(self):
        self.get_all_keys()

        for value in self.document_values_to_index:
            if value not in self.indexes:
                index = SimpleIndex(value)
            else:
                index = self.indexes[value]


            for id in self.ids:
                if self.is_document_inactive(id):
                    continue
                document = self.get_document_by_id(id)
                document_dict = self.convert_to_dict(document)

                index.index_document(id, document_dict)

                self.indexes[value] = index

    def get_all_keys(self):
        for id in self.ids:
            if self.is_document_inactive(id):
                continue
            document = self.get_document_by_id(id)
            document_dict = self.convert_to_dict(document)
            self.document_values_to_index += get_all_values_from_dict(document_dict)

    def convert_to_dict(self, document) -> dict:
        if isinstance(document, dict):
            return document
        if isinstance(document, str):
            return json.loads(document)
        return dict(document)

    def get_document_by_id(self, id):

        print(f"[DEBUG] id = {id}") if DEBUG else None
        print(f"[DEBUG] ids = {self.ids}") if DEBUG else None
        if self.is_document_inactive(id):
            raise DocumentNotFoundError(f"Document {id} not found")

        target_path = self.get_path_by_id(id)

        return self.get_document_by_path(target_path)

    def get_document_by_path(self, path):
        return JSONHandler.read_json_file(path)

    def populating_db_state(self):
        
        ids = []
        ids_collection = {}
        ids_status = {}
        for dirpath, dirnames, filenames in os.walk(self.db_path):
            for filename in filenames:
                id = filename.replace(".json","")
                ids.append(id)
                ids_collection[id] = os.path.basename(dirpath)
                ids_status[id] = DocumentStatus.ACTIVE


        self.ids = ids
        self.ids_collection = ids_collection
        self.id_status = ids_status

    def delete_document_by_id(self, id):
        # TODO: Add bulk delete functionality
        if self.is_document_inactive(id):
            print(f"Document {id} not found")
            raise DocumentNotFoundError(f"Document {id} not found")
        
        deleted_data = self.get_document_by_id(id)

        self._remove_index_for_document(id)

        print(f"Document {id} deleted")
        self.id_status[id] = DocumentStatus.SOFT_DELETE

        return True

    def _remove_index_for_document(self, id):
        document = self.get_document_by_id(id)
        for key, value in document.items():
            if value in self.indexes:
                self.indexes[value].remove_document(id)
    
    def hard_delete_document_by_id(self, id):

        target_path = self.get_path_by_id(id)
        os.remove(target_path)
        print(f"Document {id} deleted")

        self.ids.remove(id)
        del self.ids_collection[id]
        del self.id_status[id]
        return True

    def recover_document_by_id(self, id):
        if  id in self.ids and self.id_status.get(id) == DocumentStatus.SOFT_DELETE:
            self.id_status[id] = DocumentStatus.ACTIVE  
            return True
        print(f"Document {id} not found")
        raise DocumentNotFoundError(f"Document {id} not found")

    def is_document_inactive(self, id):
        return self.id_status.get(id) is None or self.id_status.get(id) == DocumentStatus.SOFT_DELETE

    def get_path_by_id(self, id):
                
        if id in self.ids_collection:
            return os.path.join(self.db_path, self.ids_collection[id], f"{id}.json")
        return os.path.join(self.db_path, f"{id}.json")

    def init_collection(self, collection_name):

        collection_path = os.path.join(self.db_path, collection_name)
        if os.path.exists(collection_path):
            print(f"[DEBUG] Collection {collection_name} already exists") if DEBUG else None
            return True
        os.mkdir(collection_path)
        return True