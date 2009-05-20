class Phrase:
    def __init__(self, items):
        """
        Values are list of words, separators
        """
        self._items = items
    def getItems(self):
        return self._items
        

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
