
from db_utils.utils import walkthrough_dict_apply_function


class SimpleIndex:
    def __init__(self, key_index):
        self.index = {}
        self.key_index = key_index

    def _index_document(self, key, value):
    
        if key == self.key_index:
            if value not in self.index:
                self.index[value] = []
            self.index[value].append(doc_id)

    def index_document(self, doc_id, data):

        walkthrough_dict_apply_function(data, self._index_document)

    def search(self, value):
        
        if value in self.index:
            return self.index[value]
        return []

    def __str__(self):
        return str(self.index)