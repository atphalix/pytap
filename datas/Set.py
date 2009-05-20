class Set:
    def __repr__(self):
        return "<set>" + str(self._value) + "</set>"

    def __str__(self):
        return self.__repr__()
