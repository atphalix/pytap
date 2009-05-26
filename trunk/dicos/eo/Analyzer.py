#!/usr/bin/python
# -*- coding: utf-8 -*-

from Constants import *
from TextExpander import TextExpander



class Analyzer:
    def __init__(self, datasFactory):
        self._datasFactory = datasFactory
        self._dicSounds = {
                "cx":"tS", "gx":"dZ", "h":"x", "jx":"Z", "sx":"S", "ux":"w", 
                "c":"ts",
                " ":"_", ".":"_", ",":"_", "-":"_", "(":"_", ")":"_",
                "\r":"_", "\n":"_",
            }
        self._facSoundsMultiply = {'x':2}
        self._lstWordSeparators = [
                "(", ")", "'", "\"", "[", "]", "{", "}",  
                "+", "@", "*", "#", "%", "&", "/", "=", "$", "£", "-", " "]
        self._lstPhraseSeparators = [",", ".", ";", "!", "?"]


    #>------------------------------------------------------------------------

    def analyze(self, text):
        print "Analyzing <<<", text, ">>>"

        # Lower text
        text = text.lower()

        # Expand text
        text = TextExpander().expand(text)

        # Create characters
        chars = self._createCharacters(text)
        print chars
        # Create words and separators
        items = self._createWordsAndSeparators(chars)
        print items

        # Create phrases
        phrases = self._createPhrases(items)
        print phrases

        # Add syllabs
        # XXX does nothing?
        #phrases = self._addSyllabsToPhrases(phrases)

        # Create pho
        pho = self._createPho(phrases)
        return pho


    #>------------------------------------------------------------------------

    def _createPho(self, phrases):
        pho = []
        for phrase in phrases:
            lpho = self._createPhoForPhrase(phrase)
            pho+=lpho
        return pho

    #>------------------------------------------------------------------------

    def _createPhoForPhrase(self, phrase):
        items = phrase.getItems()
        lstPHO=[]
        type="."
        for noItem in range(len(items)):
            item = items[noItem]
            if item.getType()==WORD:
                characters = item.getLstCharacters()
                vowels = [i for i in range(len(characters)) if characters[i].getValue() in ['a', 'e', 'i', 'o', 'u']]

                for i, character in enumerate(characters):
                    c = character.getValue()
                    # replace with phoneme
                    c = self._dicSounds.get(c, c)

                    if i==0:  # first character
                        lstPHO.append((c, voice[TIME_START], 0, voice[FREQ_START]))
                    elif len(vowels)>=2 and i==vowels[-2]: # accent
                        lstPHO.append((c, voice[TIME_ACCENT], 50, voice[FREQ_ACCENT]))
                    elif i==len(characters)-1: # end of word
                        lstPHO.append((c, voice[TIME_LAST_SOUND], 0, voice[FREQ_END_OF_WORD]))
                    else: # normal character
                        lstPHO.append((c, voice[TIME_NORMAL], 0, 0))


            elif item.getType()==WORD_SEPARATOR:
                #print "WS=",item.getValue()
                pass
            elif item.getType()==PHRASE_SEPARATOR:
                #print "PS=",item.getValue()
                c = item.getValue().getValue()
                if c=="?":
                    lstPHO.append(("_", 300, 0, voice[FREQ_EXPRESSIVE]))
                    type = c
                elif c in [".", ";"]:
                    lstPHO.append(("_", 300, 0, voice[FREQ_END_OF_PHRASE]))
                    type = c
                elif c=="!":
                    lstPHO.append(("_", 300, 0, voice[FREQ_START]))
                    type = c
                elif c==",":
                    lstPHO.append(("_", 100, 0, voice[FREQ_START]))
                    type = c
                else:
                    lstPHO.append(("_", 300, 0, 0))
            else:
                print "Unsupported item type : ", item.getType()


        # Fac sounds multiply
        i=0
        for el in lstPHO:
            if self._facSoundsMultiply.has_key(el[0]):
                tup = list(el)
                tup[1]*=self._facSoundsMultiply[el[0]]
                lstPHO = lstPHO[:i] + [tuple(tup)] + lstPHO[i+1:]
            i+=1

	
        # Intonation
        if type=="?":
            f = voice[F_QUESTION]
        elif type=="!":
            f = voice[F_EXCLAMATION]
        elif type==",":
            f = voice[F_SUBPHRASE]
        else:
            f = voice[F_NORMAL]

        i=0
        if len(lstPHO)>1:
            for el in lstPHO:
                PHOPercent = float(i)/(len(lstPHO)-1)
                if len(el)==4:
                    p, time, percent, freq = el
                    #print el, "///", 
                    freq+=f(PHOPercent)*voice[FREQ_NORMAL]
                    freq = int(freq)
                    #print p, time, percent, freq
                    lstPHO = lstPHO[:i] + [(p, time, percent, freq)] + lstPHO[i+1:]
                i+=1


        return lstPHO


    #>------------------------------------------------------------------------

    def _createCharacters(self, orig_text):
        """
        Create list of characters from plain text.
        @return list of characters
        """
        text = orig_text.replace('ĉ', 'cx').replace('ŝ', 'sx').replace('ĥ', 'hx').replace('ĝ', 'gx').replace('ŭ', 'ux').replace('ĵ', 'jx')
        lstCharacters = []
        while text!="":
            # Get next character
            c = text[0]
            text = text[1:]

            # Expand x notation
            if len(text) > 0:
                c2 = text[0]
                if c2 == "x" and c in ["c", "s", "g", "j", "u"]:
                    text = text[1:]
                    c += c2

            # Append character
            lstCharacters.append(self._datasFactory.newCharacter(c))
        return lstCharacters


    #>------------------------------------------------------------------------

    def _createWordsAndSeparators(self, characters):
        """
        Create a list of words and separators objects
        @return [(word | separator)*]
        """
        # XXX combine with phrases
        items = []
        word=[]
        for character in characters:
            cv = character.getValue()

            # Handle new character
            if cv in self._lstWordSeparators:
                # Flush word (add word to items list)
                if len(word)>0:
                    items.append(self._datasFactory.newWord(word))
                    word=[]

                # Add a new word separator
                items.append(self._datasFactory.newSeparator(character, WORD_SEPARATOR))
            elif cv in self._lstPhraseSeparators:
                # Flush word (add word to items list)
                if len(word)>0: 
                    items.append(self._datasFactory.newWord(word))
                    word=[]

                # Add a new phrase separator
                items.append(self._datasFactory.newSeparator(character, PHRASE_SEPARATOR))
            else:
                # Add character to word
                word.append(character)

        # Flush word to items list
        if len(word)>0:
            items.append(self._datasFactory.newWord(word))
        return items
                
            

    #>------------------------------------------------------------------------

    def _createPhrases(self, items):
        """
        Create phrases from items (words and separators)
        """
        import types
        phrases = []
        phrase = []
        for element in items:
            if (element.getType()==WORD):
                # Add word to phrase
                phrase.append(element)
            elif isinstance(element, types.InstanceType):
                # Add separator to phrase, flush phrase
                if element.getType()==PHRASE_SEPARATOR:
                    phrase.append(element)
                    lphrase = self._datasFactory.newPhrase(phrase)
                    phrases.append(lphrase)
                    phrase=[]
                else:
                    # Add word separator to phrase
                    phrase.append(element)
            else:
                # Unknown element
                print "?:",type(element)

        # Create a new phrase object from list of items
        if len(phrase)>0:
            lphrase = self._datasFactory.newPhrase(phrase)
            phrases.append(lphrase)
        return phrases


    #>------------------------------------------------------------------------

    def _addSyllabsToPhrases(self, phrases):
        for phrase in phrases:
            for item in phrase.getItems():
                if (item.getType()==WORD):
                    word = item
                    characters = word.getLstCharacters()
                    #for character in characters:
                        #print "c=",character.getValue()
                else:
                    print "non-word: ", item
        return phrases

