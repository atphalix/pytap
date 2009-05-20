from Character import Character
from Word import Word
from Separator import Separator
from Phrase import Phrase
from Set import Set


class DatasFactory:
    def newCharacter(self, value):
        return Character(value)

    def newWord(self, value):
        return Word(value)

    def newSeparator(self, value, type):
        return Separator(value, type)

    def newPhrase(self, value):
        return Phrase(value)

    def newSet(self, value):
        return Set(value)
