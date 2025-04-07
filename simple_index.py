
from db_utils.utils import walkthrough_dict_apply_function


class SimpleIndex:
    def __init__(self, key_index):
        self.index = {}
        self.key_index = key_index
        self._current_doc_id = None

    def _index_document(self, key, value):
        if value == self.key_index:
            if value not in self.index:
                self.index[value] = []

            if self._current_doc_id not in self.index[value]:
                self.index[value].append(self._current_doc_id)

    def index_document(self, doc_id, data):

        self._current_doc_id = doc_id
        walkthrough_dict_apply_function(data, self._index_document)

    def search(self, value):
        
        if value in self.index:
            return self.index[value]
        return []

    def remove_document(self, doc_id):
        keys_to_check = []

        for key in self.index:
            if doc_id in self.index[key]:
                self.index[key].remove(doc_id)
                keys_to_check.append(key)

        for key in keys_to_check:
            if len(self.index[key]) == 0:
                del self.index[key]

    def __str__(self):
        return str(self.index)

    def __repr__(self):
        return str(self.index)

    def __len__(self):
        return len(self.index)