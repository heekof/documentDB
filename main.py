import uuid
import json
import os

from json_handler import JSONHandler
from simple_document_db import SimpleDocumentDB


db = SimpleDocumentDB()

id_jaafar = db.insert_one("users", {"name": "Jaafar", "age": 34})
id_ikram = db.insert_one("users", {"name": "Ikram", "age": 30})

id_yasmina = db.insert_one("users", json.loads('{"name": "Yasmina", "age": 30}'))

name_index = {
    "Jaafar": ["uuid1", "uuid2", "uuid3"],
    "Ikram": ["uuid4", "uuid5"]
}

db.indexing_documents()

for k,v in db.indexes.items():
    print(k, v.index)