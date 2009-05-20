import math

WORD_SEPARATOR = 1
PHRASE_SEPARATOR = 2
WORD = 10

# Voice definition : 
# Time are in mSec
# Freq is in ??? (FREQ_NORMAL is absolute, others are relative to porteuse)
# F_XXX is Function of phrase percentil(0-1), which results will be multiplied
# to pho frequency.

TIME_NORMAL = 20
TIME_ACCENT = 21
TIME_LAST_SOUND = 22
TIME_LINK = 23
TIME_START = 24
FREQ_NORMAL = 30
FREQ_EXPRESSIVE = 31
FREQ_ACCENT = 32
FREQ_END_OF_PHRASE = 33
FREQ_START = 34
FREQ_END_OF_WORD=35
F_NORMAL = 40
F_QUESTION = 41
F_EXCLAMATION = 42
F_SUBPHRASE = 43  #xxxxx,

#((normal time, accent time, last sound time, link time, start time),
# (normal freq, expressive freq, accent freq, end-of-phrase freq, start freq))
#voice1 = ((100, 180, 200, 1, 80), (180, 330, 200, 126, 150, 170))
#voice1 = ((100, 180, 200, 1, 80), (200, 220, 200, 126, 170, 170))
voice = {
        TIME_NORMAL:100,
        TIME_ACCENT:180,
        TIME_LAST_SOUND:200,
        TIME_LINK:1,
        TIME_START:80,
        FREQ_NORMAL:200,
        FREQ_EXPRESSIVE:20,
        FREQ_ACCENT:10,
        FREQ_END_OF_PHRASE:-50,  #-74
        FREQ_START:-30,
        FREQ_END_OF_WORD:-30,
        #F_NORMAL:lambda x:math.cos(x*1.4)**0.5,
        #F_NORMAL:lambda x:math.cos(x*1.4)**0.5 + math.sin(x*30)/100.0,
        F_NORMAL:lambda x:math.cos(x*1.4)**0.2 + math.sin(x*10)/100.0,
        F_QUESTION:lambda x:((x*2-0.8)**2)/8.0+7.0/8.5,
        F_EXCLAMATION:lambda x:((x*2-1.2)**2)/8.0+7.0/8.0 + math.cos(x*3.0)-math.cos(x*3.9),
        F_SUBPHRASE:lambda x:math.sin(x+0.95),
}

# TODO : replace freq by +10, -10, ... from normal freq
# TODO : expressions : 
# normal   = cos[0,70]
# question = t[-1, 1]^2/2+1/2
# exclamation = t[-1, 1]^2/8+7/8


#voice1 = ((100, 180, 100, 1, 100), (160, 330, 170, 170, 150))
#voice1 = ((80, 180, 200, 1, 80), (160, 330, 180, 130, 190))
#voice1 = ((80, 180, 200, 1, 80), (180, 330, 200, 170, 160))
