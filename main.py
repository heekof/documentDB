import uuid
import json
import os

from json_handler import JSONHandler
from simple_document_db import SimpleDocumentDB


db = SimpleDocumentDB()

doc_id = db.insert_one("users", {"name": "Jaafar", "age": 34})

db.update_document_by_id("users", {"name": "Jaafar", "age": 35}, doc_id)

for k,v in db.indexes.items():
    print(v.index)