# Simple Document DB

## Project Overview

This is a personal learning project aimed at creating a simple document database engine in Python. The main goal is to understand the fundamental concepts of database management systems, JSON handling, and Python programming.

## Project Structure

The project consists of three main Python files:

1. `simple_document_db.py`: Contains the [SimpleDocumentDB](cci:2://file:///home/bendrisj/documentDB/simple_document_db.py:13:0-149:19) class, which is the core of the database engine.
2. `json_handler.py`: Houses the [JSONHandler](cci:2://file:///home/bendrisj/documentDB/json_handler.py:8:0-55:55) class, responsible for JSON-related operations.
3. `main.py`: The entry point of the application, demonstrating usage of the database engine.

## Features

* **Collection Management**: Collections are automatically created as directories when the first document is inserted [cite: uploaded:documentDB/simple_document_db.py].
* **Document CRUD Operations**:
    * **Create**: Insert documents (Python dictionaries or JSON strings) into collections (`insert_one`) [cite: uploaded:documentDB/simple_document_db.py]. Documents are assigned a unique UUID.
    * **Read**: Retrieve documents by their unique ID (`get_document_by_id`) [cite: uploaded:documentDB/simple_document_db.py].
    * **Update**: Modify existing documents by ID (`update_document_by_id`) [cite: uploaded:documentDB/simple_document_db.py]. Supports partial updates.
    * **Delete**:
        * Soft delete documents (`delete_document_by_id`), marking them as inactive but keeping the file [cite: uploaded:documentDB/simple_document_db.py].
        * Hard delete documents (`hard_delete_document_by_id`), permanently removing the file [cite: uploaded:documentDB/simple_document_db.py].
        * Recover soft-deleted documents (`recover_document_by_id`) [cite: uploaded:documentDB/simple_document_db.py].
* **Basic Querying**: Find documents within a collection based on simple key-value equality (`find`) [cite: uploaded:documentDB/simple_document_db.py].
* **File-Based Storage**: Each document is stored as a separate `.json` file within its collection's directory [cite: uploaded:documentDB/simple_document_db.py].
* **Configuration**: Basic settings can be managed via `settings.json` [cite: uploaded:documentDB/settings.json, uploaded:documentDB/global_state.py].
* **Custom Errors**: Specific error types for issues like `DocumentNotFoundError` [cite: uploaded:documentDB/errors.py].


## Key Features

- Document insertion and retrieval
- Basic querying capabilities
- JSON data handling
- File-based storage system

## Learning Objectives

Through this project, you can learn about:

1. Database Design: Understanding how to structure a simple database system.
2. JSON Handling: Working with JSON data in Python.
3. File I/O: Managing file operations for data persistence.
4. Error Handling: Implementing custom exceptions and error management.
5. Code Organization: Structuring a Python project with multiple modules.

## Future Improvements

To enhance your learning experience, consider implementing these features:

1. Advanced Querying: Add support for complex queries (regex, comparisons).
2. Indexing: Implement a basic indexing system to improve query performance.
3. Concurrency: Add support for multiple simultaneous database operations.
4. Data Validation: Implement schema validation for documents.
5. Transactions: Add support for atomic operations across multiple documents.

## Getting Started

1. Clone this repository
2. Run `main.py` to see the database in action
3. Explore the code in `simple_document_db.py` and `json_handler.py`
4. Start implementing new features or optimizations!

## Contributing

As this is a personal learning project, contributions are not expected. However, feel free to fork this project and adapt it for your own learning journey!

## TODO

1. Create a Simple Query Language (SQL-lite style)
'''results = db.find("users", query="age > 30 AND name == 'Jaafar'")'''

2. Implement Versioning for Documents
''' db.rollback_document(id, version=1)'''

3. Add Optional Encryption Support
''' db.insert_one("users", {"name": "Ikram"}, encrypt=True) '''

4. Implement an Indexing System

'''
name_index = {
    "Jaafar": ["uuid1", "uuid2", "uuid3"],
    "Ikram": ["uuid4", "uuid5"]
}
'''

5. Implement Data Validation (Schema Validation):

For example, you could define that documents in the "users" collection must have a "name" (string) and an "age" (integer). Your insert_one and update_document_by_id methods should then validate incoming data against the schema before saving it 


6.  Add a RESTful API Layer
'''
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
db = SimpleDocumentDB()

@app.get("/collections/{collection_name}/documents/{doc_id}")
def get_document(collection_name: str, doc_id: str):
    return db.get_document_by_id(doc_id)
'''