import Constants

class Separator:
    def __init__(self, value, type):
        self._value = value
        self._type = type

    def __repr__(self):
        type = "?"
        if (self._type==Constants.WORD_SEPARATOR):
            type="ws"
        elif (self._type==Constants.PHRASE_SEPARATOR):
            type="ps"
        return "<separator type='%s'>" % (type) + str(self._value) + \
                "</separator>"

    def __str__(self):
        return self.__repr__()

    def getValue(self):
        return self._value

    def getType(self):
        return self._type
