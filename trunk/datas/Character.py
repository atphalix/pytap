class Character:

    def __init__(self, value):
        self._value = value

    def getValue(self):
        return self._value
        



    def __repr__(self):
        return "<character>" + str(self._value) + "</character>"
    def __str__(self):
        return self.__repr__()
