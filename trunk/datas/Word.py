import Constants
class Word:
    def __init__(self, lstCharacters):
        self._lstCharacters = lstCharacters
    def getLstCharacters(self):
        return self._lstCharacters

    def getType(self):
        return Constants.WORD

    def __repr__(self):
        return "<word>" + str(self._lstCharacters) + "</word>"
    def __str__(self):
        return self.__repr__()
