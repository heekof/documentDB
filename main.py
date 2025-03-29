class SimpleDocumentDB:
    def __init__(self, db_path="mydb"):
        ...

    def create_collection(self, name):
        ...

    def insert_one(self, collection, document):
        """
        if collection in collections, check document and then add it.
        """
        ...

    def find(self, collection, query=None):
        ...

    def update_one(self, collection, query, update_fields):
        ...

    def delete_one(self, collection, query):
        ...

db = SimpleDocumentDB()

db.insert_one("users", {"name": "Jaafar", "age": 34})
results = db.find("users", {"age": 34})
