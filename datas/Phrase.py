class Phrase:
    """Values are list of words, separators"""
    def __init__(self, items):
        self._items = items

    def __repr__(self):
        import types
        s="<phrase>"
        for item in self._items:
            s+="<item>"
            if isinstance(item, types.ListType):
                s+="<chars>"
                for c in item:
                    s+=str(c)
                s+="</chars>"
            else:
                s+=str(item)
            s+="</item>"
        s+="</phrase>"
        return s

    def __str__(self):
        return self.__repr__()

    def getItems(self):
        return self._items
