import uuid
import json
import os

from json_handler import JSONHandler
from simple_document_db import SimpleDocumentDB


db = SimpleDocumentDB()

id_jaafar = db.insert_one("users", {"name": "Jaafar", "age": 34})
id_ikram = db.insert_one("users", {"name": "Ikram", "age": 30})

id_yasmina = db.insert_one("users", json.loads('{"name": "Yasmina", "age": 30}'))

print(f"Jaafar's id = {id_jaafar}")
print(f"Ikram's id = {id_ikram}")
print(f"Yasmina's id = {id_yasmina}")



db.update_document_by_id(
    collection_name = "users", 
    data = {"age": 61}, 
    id = id_ikram
    )