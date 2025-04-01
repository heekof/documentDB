import unittest
import os
import shutil
from simple_document_db import SimpleDocumentDB
import json
from errors import DocumentNotFoundError

class TestSimpleDocumentDB(unittest.TestCase):

    def setUp(self):
        # Setup a clean test database directory
        self.test_db_path = "test_db"
        if os.path.exists(self.test_db_path):
            shutil.rmtree(self.test_db_path)
        os.makedirs(self.test_db_path)

        self.db = SimpleDocumentDB(db_path=self.test_db_path)

    def tearDown(self):
        # Clean up the test directory after each test
        shutil.rmtree(self.test_db_path)

    def test_insert_and_find(self):
        doc_id = self.db.insert_one("users", {"name": "Jaafar", "age": 34})
        results = self.db.find("users", {"name": "Jaafar"})

        self.assertEqual(len(results), 1)

        for result in results :
            self.assertEqual(result[doc_id]["age"], 34)

    def test_insert_and_find_multiple(self):
        doc_id1 = self.db.insert_one("users", {"name": "Jaafar", "age": 34})
        doc_id2 = self.db.insert_one("users", {"name": "Jaafar", "age": 34})
        doc_id3 = self.db.insert_one("users", {"name": "Jaafar", "age": 34})
        results = self.db.find("users", {"name": "Jaafar"})

        self.assertEqual(len(results), 3)

    def test_insert_and_find_str(self):

        id_yasmina = self.db.insert_one("users", json.loads('{"name": "Yasmina", "age": 30}'))
        results = self.db.find("users", {"age": 30})

        for result in results :
            self.assertEqual(result[id_yasmina]["name"], "Yasmina")


    def test_get_document_by_id_not_found(self):
        with self.assertRaises(DocumentNotFoundError):
            self.db.get_document_by_id("c547e6bd-d291-482e-9e5d-6164211cff7d")


    def test_get_document_by_id_found(self):
        doc_id = self.db.insert_one("users", {"name": "Ikram", "age": 30})
        doc = self.db.get_document_by_id(doc_id)
        self.assertEqual(doc["name"], "Ikram")

    def test_update_document_by_id(self):
        doc_id = self.db.insert_one("users", {"name": "Ikram", "age": 30})
        self.db.update_document_by_id("users", {"name": "Ikram", "age": 31}, doc_id)
        updated_doc = self.db.get_document_by_id(doc_id)
        self.assertEqual(updated_doc["age"], 31)

    def test_delete_document_by_id(self):
        doc_id = self.db.insert_one("users", {"name": "Ikram", "age": 30})
        self.db.delete_document_by_id(doc_id)
        with self.assertRaises(DocumentNotFoundError):
            self.db.get_document_by_id(doc_id)

    def test_get_document_by_id(self):
        doc_id = self.db.insert_one("users", {"name": "Ikram", "age": 30})
        doc = self.db.get_document_by_id(doc_id)
        self.assertEqual(doc["name"], "Ikram")

    def test_update_document_by_id(self):
        doc_id = self.db.insert_one("users", {"name": "Ikram", "age": 30})
        self.db.update_document_by_id("users", {"name": "Ikram", "age": 31}, doc_id)
        updated_doc = self.db.get_document_by_id(doc_id)
        self.assertEqual(updated_doc["age"], 31)

if __name__ == '__main__':
    unittest.main()
    # python -m unittest discover -s tests
