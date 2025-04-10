import unittest
import os
import shutil
from simple_document_db import SimpleDocumentDB
import json
from errors import DocumentNotFoundError

class TestSimpleDocumentDB(unittest.TestCase):

    _sample_data = {
        "name": "Jaafar",
        "age": 34,
        "city": "Paris",
        "country": "France"
    }

    _sample_data2 = """{
        "name": "Ikram",
        "age": 30,
        "city": "Paris",
        "country": "France"
    }"""

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

        id_yasmina = self.db.insert_one("users", '{"name": "Yasmina", "age": 30}')
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

    def test_update_document_by_id_check_all(self):
        doc_id = self.db.insert_one("users", {"name": "Ikram", "age": 30})
        self.db.update_document_by_id("users", {"name": "Ikram", "age": 31}, doc_id)
        updated_doc = self.db.get_document_by_id(doc_id)
        self.assertEqual(updated_doc, {"name": "Ikram", "age": 31})    

    def test_hard_delete_document_by_id(self):
        doc_id = self.db.insert_one("users", {"name": "Ikram", "age": 30})
        self.db.hard_delete_document_by_id(doc_id)
        with self.assertRaises(DocumentNotFoundError):
            self.db.get_document_by_id(doc_id) 

        with self.assertRaises(DocumentNotFoundError):
            self.db.recover_document_by_id(doc_id)


    def test_soft_delete_document_by_id(self):
        doc_id = self.db.insert_one("users", self._sample_data)
        self.db.delete_document_by_id(doc_id)

        with self.assertRaises(DocumentNotFoundError):
            self.db.get_document_by_id(doc_id)

        self.db.recover_document_by_id(doc_id)
        doc = self.db.get_document_by_id(doc_id)
        self.assertEqual(doc, self._sample_data)


    def test_index_document(self):
        doc_id = self.db.insert_one("users",{ "name": "Jaafar", "age": 34})
        results = self.db.indexes["Jaafar"]
        r_id = results.index['Jaafar'][0]
        self.assertEqual(r_id, doc_id)

    def test_index_after_deleting_document(self):
        doc_id = self.db.insert_one("users",{ "name": "Jaafar", "age": 34})
        self.db.delete_document_by_id(doc_id)
        print(f"[DEBUG] indexes = {self.db.indexes.keys()}")
        print(f"[DEBUG] indexes = {self.db.indexes[34]}")
        print(f"[DEBUG] indexes = {self.db.indexes['Jaafar']}")
        # print(f"[DEBUG] indexes = {self.db.indexes["Jaafar"]}")
        self.assertEqual(len(self.db.indexes[34]), 0)
        self.assertEqual(len(self.db.indexes['Jaafar']), 0)

    def test_index_after_updating_document(self):
        doc_id = self.db.insert_one("users",{ "name": "Jaafar", "age": 34})
        self.db.update_document_by_id("users", {"name": "Jaafar", "age": 35}, doc_id)
        self.assertEqual(len(self.db.indexes[34]), 0)
        self.assertEqual(len(self.db.indexes[35]), 1)

if __name__ == '__main__':
    unittest.main()
    # python -m unittest discover -s tests
