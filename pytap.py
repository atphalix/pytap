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

def synthesizePho(file, voice, output_file):
    """Generate sound from phoneme file with voice"""
    cmd = """cat "%s" | mbrola/mbrola-linux-i386 mbrola/%s/%s - %s""" % (file, voice, voice, output_file)
    os.system(cmd)
  


if __name__=="__main__":
    from optparse import OptionParser
    parser = OptionParser('usage: %prog -t text | -f file | -p phoneme [-o output] [-v voice] [-l language] [-r]')
    parser.add_option('-t', '--text', dest='text', default='', help='Specify text to render')
    parser.add_option('-f', '--file', dest='file', default='', help='Choose file to read')
    parser.add_option('-p', '--phoneme', dest='phoneme', default='', help='Choose a pho file')
    parser.add_option('-o', '--output', dest='output', default='sound.wav', help='Specify output file for sound')
    parser.add_option('-v', '--voice', dest='voice', default='pl1', help='Choose voice')
    parser.add_option('-l', '--language', dest='language', default='eo', help='Choose language {eo}')
    parser.add_option('-r', '--run', dest='run', action='store_true', default=False, help='Play sound that was rendered')
    options, args = parser.parse_args()

    if options.text:
        options.phoneme = generatePho(options.text)
    elif options.file:
        text = open(options.file).read()
        options.phoneme = generatePho(text)
    elif options.phoneme:
        pass # have specified phoneme file
    else:
        parser.print_help()
        sys.exit()

    synthesizePho(options.phoneme, options.voice, options.output)
    if options.run:
        # play sound
        os.system('play %s' % options.output)
