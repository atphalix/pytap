#!/usr/bin/python
# -*- coding: utf-8 -*-


from Constants import *
from TextExpander import TextExpander
voice = voice1

class Analyzer:
    def __init__(self, datasFactory):
        self._datasFactory = datasFactory
        self._dicSounds = {
                "cx":"tS", "gx":"dZ", "h":"x", "jx":"Z", 
                "sx":"S", "ux":"w", 
                " ":"_", ".":"_", ",":"_", "-":"_", "(":"_", ")":"_",
                "\r":"_", "\n":"_",
                "c":"ts"
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

        # Create words and separators
        items = self._createWordsAndSeparators(chars)

        # Create phrases
        phrases = self._createPhrases(items)

        # Add syllabs
        phrases = self._addSyllabsToPhrases(phrases)

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
        import types
        #print "======================================================="
        #print phrase

        items = phrase.getItems()
        lstPHO=[]
        type="."
        for noItem in range(len(items)):
            item = items[noItem]
            if item.getType()==WORD:
                characters = item.getLstCharacters()
                voyelles = [i  for i in range(len(characters))
                               if characters[i].getValue() 
                               in ['a', 'e', 'i', 'o', 'u']]

                for i in range(len(characters)):
                    character = characters[i]
                    c = character.getValue()
                    if self._dicSounds.has_key(c):
                        c = self._dicSounds[c]
                    if i==0:  # First
                        lstPHO.append((c, voice[TIME_START], 0, voice[FREQ_START]))
                    #elif i==len(characters)-5:
                        # Hack to get last last syllab; to improve
                        #lstPHO.append((c, voice[0][0], 50, voice[1][0]))
                    elif len(voyelles)>=2 and i==voyelles[-2]-1: # before accent
                        # Hack to get last syllab; to improve
                        lstPHO.append((c, voice[TIME_NORMAL], 0, 0))
						# FREQ_NORMAL todo
                    elif len(voyelles)>=2 and i==voyelles[-2]: # accent
                        # Hack to get last syllab; to improve
                        lstPHO.append((c, voice[TIME_ACCENT], 50, voice[FREQ_ACCENT]))
                    #elif i==2 and len(voyelles)>2:
                        #lstPHO.append((c, voice[0][4], 100, voice[1][0]))
                    #elif i==len(characters)-1:
                        #lstPHO.append((c, voice[0][2], 50, voice[1][5]))
                    else:
                        lstPHO.append((c, voice[TIME_NORMAL]))
                    #fin de phrase plus longue !


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
                print "Unsuppored item type : ", item.getType()


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









    def old(self):

        # OLD

        lstPHO=[]
        items = phrase.getItems()
        for noItem in range(len(items)):
            item = items[noItem]
            if (item.getType()==WORD):
                # Add words
                characters = item.getLstCharacters()
                voyelles = [i  for i in range(len(characters))
                               if characters[i].getValue() 
                               in ['a', 'e', 'i', 'o', 'u']]
                for i in range(len(characters)):
                    character = characters[i]
                    c = character.getValue()
                    if self._dicSounds.has_key(c):
                        c = self._dicSounds[c]
                    if i==0:
                        lstPHO.append((c, 100, 0, 130))
                    else:
                        if i==len(characters)-5:
                            # Hack to get last syllab; to improve
                            lstPHO.append((c, 100, 0, 120))
                        elif len(voyelles)>=2 and i==voyelles[-2]:
                            # Hack to get last syllab; to improve
                            lstPHO.append((c, 140, 50, 130))
                        else:
                            lstPHO.append((c, 100))

                # Frequency for .?!
                #print "NI ", noItem, len(items), str(items[noItem])
                #if noItem==len(items)-2:
                    #nextItem = items[noItem+1]
                    #print "NI=" + str(nextItem)
                    
            else:
                lstPHO.append(("_", 30, 100, 110))

        # Intonation
        

        # Intonation
        #tuple = lstPHO[0]
        #lstPHO = [(tuple[0], tuple[1], "0", "130")] + lstPHO[1:]
        #tuple = lstPHO[-1]
        #lstPHO = lstPHO[:-1] + [(tuple[0], tuple[1], "100", "80")]


        # convert PHO to text
        pho=""
        for el in lstPHO:
            line=""
            for el2 in el:
                line+=str(el2) + " "
            pho+=line + "\n"

        return pho



    #>------------------------------------------------------------------------

    def _createPhoForPhraseOld(self, phrase):
        import types
        print "======================================================="
        print phrase
        lstPHO=[]
        items = phrase.getItems()
        for noItem in range(len(items)):
            item = items[noItem]
            if (item.getType()==WORD):
                # Add words
                characters = item.getLstCharacters()
                voyelles = [i  for i in range(len(characters))
                               if characters[i].getValue() 
                               in ['a', 'e', 'i', 'o', 'u']]
                for i in range(len(characters)):
                    character = characters[i]
                    c = character.getValue()
                    if self._dicSounds.has_key(c):
                        c = self._dicSounds[c]
                    if i==0:
                        lstPHO.append((c, 100, 0, 130))
                    else:
                        if i==len(characters)-5:
                            # Hack to get last syllab; to improve
                            lstPHO.append((c, 100, 0, 120))
                        elif len(voyelles)>=2 and i==voyelles[-2]:
                            # Hack to get last syllab; to improve
                            lstPHO.append((c, 140, 50, 130))
                        else:
                            lstPHO.append((c, 100))

                # Frequency for .?!
                #print "NI ", noItem, len(items), str(items[noItem])
                #if noItem==len(items)-2:
                    #nextItem = items[noItem+1]
                    #print "NI=" + str(nextItem)
                    
            else:
                lstPHO.append(("_", 30, 100, 110))


        # Intonation
        tuple = lstPHO[0]
        lstPHO = [(tuple[0], tuple[1], "0", "130")] + lstPHO[1:]
        tuple = lstPHO[-1]
        lstPHO = lstPHO[:-1] + [(tuple[0], tuple[1], "100", "80")]


        # convert PHO to text
        pho=""
        for el in lstPHO:
            line=""
            for el2 in el:
                line+=str(el2) + " "
            pho+=line + "\n"

        return pho
        #for chars in phrase:
        #    v = chars2.pop(0).getValue()
        #    if self._dicSounds.has_key(v):
        #        v = self._dicSounds[v]
        #    pho+=v + " 120 50 100\n"

        #    while len(chars2)>0:
        #        # Get next diphone
        #        v2 = chars2[0].getValue()
        #        if self._dicSounds.has_key(v2):
        #            v2 = self._dicSounds[v2]

        #        if v=="n" and v2=="c":
        #            v2="_"
        #            chars2 = [self._datasFactory.newCharacter(" ")] + chars2

        #        # Break
        #        if v2!=v and v2 not in [".", "?", "!"]: break
        #        chars2.pop(0)



    #>------------------------------------------------------------------------

    def _createCharacters(self, text):
        """
        Create list of characters from plain text.
        @return list of characters
        """
        txt = text[:]
        lstCharacters = []
        while txt!="":
            # Get next character
            c = txt[0]
            txt = txt[1:]

            # Expand x notation
            if len(txt)>0:
                c2 = txt[0]
                if c2 == "x" and c in ["c", "s", "g", "j", "u"]:
                    txt = txt[1:]
                    c = c + c2

            # Append character
            lstCharacters.append(self._datasFactory.newCharacter(c))
        return lstCharacters


    #>------------------------------------------------------------------------

    def _createWordsAndSeparators(self, characters):
        """
        Create a list of words and separators objects
        @return [(word | separator)*]
        """
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
                items.append(self._datasFactory.newSeparator(character, 
                        WORD_SEPARATOR))
            elif cv in self._lstPhraseSeparators:
                # Flush word (add word to items list)
                if len(word)>0: 
                    items.append(self._datasFactory.newWord(word))
                    word=[]

                # Add a new phrase separator
                items.append(self._datasFactory.newSeparator(character, 
                        PHRASE_SEPARATOR))
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
        import types
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



