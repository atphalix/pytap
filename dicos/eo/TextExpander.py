class TextExpander:

    def __init__(self):
        self._dicTextExpand = {
                "0":"zero ",
                "1":"unu ",
                "2":"du ", 
                "3":"tri ",
                "4":"kvar ",
                "5":"kvin ",
                "6":"ses ",
                "7":"sepe ",
                "8":"ok ",
                "9":"nauxe ",
                "ftp":"fotopo",
                "+":"pli",
                "-":"malpli",
                "s-ro":"sinjoro",
                "k-do":"kamarado",
                "d-rino":"doktorino",
                "s-ano":"samideano",
                "vd.":"vidu",
                "ekz.":"ekzemple",
                "ekz-e":"ekzemple",
                "k.t.p.":"kaj tiel plu",
                "ktp.":"kaj tiel plu",
                "t.e.":"tio estas",
                "k.a.":"kaj aliaj",
                "k.s.":"kaj simile",
                "e-o":"esperanto",
                "gdr":"germana demokratia respubliko",
                "uea ":"universala esperanto asocio ",
                "set ":"somera esperanto tendaro ",
            }


    def expand(self, txt):
        for key, value in self._dicTextExpand.items():
            txt = txt.replace(key, " " + value + " ")
        return txt
        
