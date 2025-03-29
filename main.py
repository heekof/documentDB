import uuid
import json
import os

from db_utils import db_utils as util
from simple_document_db import SimpleDocumentDB




db = SimpleDocumentDB()

#db.insert_one("users", {"name": "Jaafar", "age": 34})
results = db.find("users", {"age": 34})


random_uuid = util.get_random_uuid()
print(random_uuid)
#util.create_json_file_based_on_name(random_uuid,source_db=db,collection_name="default")

data = db.get_document_by_id("c547e6bd-d291-482e-9e5d-6164211cff7d")

print(data)