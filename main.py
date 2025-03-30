import uuid
import json
import os

from json_handler import JSONHandler
from simple_document_db import SimpleDocumentDB
from global_state import DEBUG


db = SimpleDocumentDB()

id_jaafar = db.insert_one("users", {"name": "Jaafar", "age": 34})
id_ikram = db.insert_one("users", {"name": "Ikram", "age": 30})

id_yasmina = db.insert_one("users", json.loads('{"name": "Yasmina", "age": 30}'))

print(f"Jaafar's id = {id_jaafar}")
print(f"Ikram's id = {id_ikram}")
print(f"Yasmina's id = {id_yasmina}")

results = db.find("users", {"age": 30})

data = db.get_document_by_id("c547e6bd-d291-482e-9e5d-6164211cff7d")

print(f" Result = {results}")

db.update_document_by_id(
    collection_name = "users", 
    data = {"name": "Ikram", "age": 31}, 
    id = "c547e6bd-d291-482e-9e5d-6164211cff7d"
    )