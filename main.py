import uuid
import json
import os

from json_handler import JSONHandler
from simple_document_db import SimpleDocumentDB
from global_state import DEBUG

# TODO : implement the find method in the SimpleDocumentDB class

db = SimpleDocumentDB()

#db.insert_one("users", '{"name": "Jaafar", "age": 34}')
#db.insert_one("users", {"name": "Ikram", "age": 30})

results = db.find("users", {"age": 30})


#util.parse_data(random_uuid,source_db=db,collection_name="default")

# data = db.get_document_by_id("c547e6bd-d291-482e-9e5d-6164211cff7d")

print(f" Result = {results}")