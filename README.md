# Simple Document DB : personal project

Hello, this is a personal project for a document DB engine



#  TODO

In update_ids_map(), you scan the entire directory structure on each database operation. This will become a major performance bottleneck as your database grows. Consider:

- Maintaining an in-memory index that's updated only when documents are added/removed
- Creating an index file that persists between sessions
- Using a more efficient lookup strategy than walking the entire directory tree


# Separation of Concerns (DB Logic vs. JSON Handling):

Problem: The JSONHandler.parse_data static method is doing quite a bit of database logic. It generates the ID (using get_random_uuid), determines the storage path, calls source_db.init_collection (creating coupling back to the DB instance), and finally writes the file. The SimpleDocumentDB.insert_one method essentially just delegates everything to it.

Improvement: Move the core database insertion logic into SimpleDocumentDB.insert_one.

- insert_one should:

- Generate the UUID.

- Ensure the collection directory exists (calling self.init_collection or similar internal logic).

- Determine the final file path.

- Call JSONHandler.write_json_file to simply handle the writing of the validated data to the specific path.

 - Update the internal state (like self.ids and self.ids_collection as suggested in point 1).

JSONHandler should focus purely on JSON tasks: validating JSON compatibility (is_json_compatible), reading JSON from a file (read_json_file), and writing Python objects to a JSON file (write_json_file).