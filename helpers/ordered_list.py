

def number_comparator(a, b):
    return a - b


class OrderedList:
    _elements = []
    
    def __init__(self, comparator=number_comparator, elements=None):
        if elements is not None:
            self._elements = elements
        self._comparator = comparator

    def insert(self, obj):
        self._elements.insert(self._insert_index(self._elements, obj), obj)

    def remove(self, item):
        index = self.index(item)
        if index != -1:
            self._elements.pop(index)
    
    def _insert_index(self, list_part, obj):
        if len(list_part) == 0:
            return 0
        if len(list_part) == 1:
            return int(self._comparator(obj, list_part[0]) > 0)
        
        mid = len(list_part) // 2
        if self._comparator(obj, list_part[mid]) > 0:
            return mid + self._insert_index(list_part[mid:], obj)
        else:
            return self._insert_index(list_part[:mid], obj)
    
    def index(self, obj):
        return self._dich_index(self._elements, obj)
    
    def _dich_index(self, list_part, obj, start_index=0):
        if len(list_part) == 0:
            return -1
        if len(list_part) == 1:
            return start_index if obj == list_part[0] else -1
        
        mid = len(list_part) // 2
        if self._comparator(obj, list_part[mid]) > 0:
            return self._dich_index(list_part[:mid], obj, start_index + mid)
        else:
            return self._dich_index(list_part[mid:], obj, start_index)
    
    def min(self):
        if len(self._elements) == 0:
            raise IndexError("La liste est vide")
        return self._elements[0]
    
    def max(self):
        if len(self._elements) == 0:
            raise IndexError("La liste est vide")
        return self._elements[-1]
    
    def __iter__(self):
        return self._elements.__iter__()
    
    def __len__(self):
        return len(self._elements)
    
    def __contains__(self, item):
        return self.index(item) != -1
