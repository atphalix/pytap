#
# XATUM Version 1, Copyright (C) 2005 C.Dutoit - dutoitc@shimbawa.ch
# XATUM comes with ABSOLUTELY NO WARRANTY; This is free software, 
# and you are welcome to redistribute it under certain conditions; 
#

import sys
import os
import dicos.eo.Analyzer as dic
import datas.DatasFactory


def generatePho(text):
    """Generate phoneme file for text, and return filename"""
    analyzer = dic.Analyzer(datas.DatasFactory.DatasFactory())
    phonemes = []
    for phoneme in analyzer.analyze(text):
        phonemes.append(' '.join(str(data) for data in phoneme))

    # write phoneme to output file
    output_file = 'tmp.pho'
    open(output_file, 'w').write('\n'.join(phonemes))
    return output_file

def synthesizePho(file, voice, output_file, pitch, speed):
    """Generate sound from phoneme file with voice"""
    cmd = """cat "%s" | mbrola/mbrola-linux-i386 -e -f %f -t %f mbrola/%s/%s - %s""" % (file, pitch, speed, voice, voice, output_file)
    print cmd
    os.system(cmd)
  

def availableVoices():
    """Each voice has the directory structure mbrola/voice/voice"""
    voices = []
    for file in os.listdir('mbrola'):
        if os.path.exists(os.path.join('mbrola', file, file)):
            voices.append(file)
    return voices
def availableLanguages():
    """Each langauge has the directory structure dicos/voice/__init__.py"""
    languages = []
    for file in os.listdir('dicos'):
        if os.path.exists(os.path.join('dicos', file, '__init__.py')):
            languages.append(file)
    return languages



def main():
    from optparse import OptionParser
    parser = OptionParser('usage: %prog -t text | -f file | -p phoneme [-o output] [-v voice] [-l language]')
    parser.add_option('-t', '--text', dest='text', default='', help='Specify text to render')
    parser.add_option('-f', '--file', dest='file', default='', help='Choose file to read')
    parser.add_option('-p', '--phoneme', dest='phoneme', default='', help='Choose a pho file')
    parser.add_option('-o', '--output', dest='output', default='sound.wav', help='Specify output file for sound')
    parser.add_option('-v', '--voice', dest='voice', default='pl1', help='Choose voice')
    parser.add_option('-l', '--language', dest='language', default='eo', help='Choose language')
    parser.add_option('--pitch', dest='pitch', default=1.0, help='Ratio applied to pitch of voice (default 1.0)')
    parser.add_option('--speed', dest='speed', default=1.0, help='Ratio applied to speed of voice (default 1.0)')
    parser.add_option('--play', dest='play', action='store_true', default=False, help='Play sound that was rendered')
    parser.add_option('--voices', dest='voices', action='store_true', default=False, help='Display a list of all available voices')
    parser.add_option('--languages', dest='languages', action='store_true', default=False, help='Display a list of all available languages')
    options, args = parser.parse_args()

    if options.voices:
        print '\n'.join(availableVoices())
    elif options.languages:
        print '\n'.join(availableLanguages())
    else:    
        # synthesize voice
        if not sys.stdin.isatty():
            # input is being piped
            options.phoneme = generatePho(sys.stdin.read())
        elif options.text:
            options.phoneme = generatePho(options.text)
        elif options.file:
            text = open(options.file).read()
            options.phoneme = generatePho(text)
        elif options.phoneme:
            pass # have specified phoneme file
        else:
            parser.print_help()
            return

        synthesizePho(options.phoneme, options.voice, options.output, float(options.pitch), float(options.speed))
        if options.play:
            # play sound
            os.system('play %s' % options.output)



if __name__=="__main__":
    main()
