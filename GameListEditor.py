#!/usr/bin/python3
# This hack adds the image, video and marquee elements to the gamelist.xml file if they exist.
# To run: python <path to addMedia.py>/addMedia.py <path to rom folder>.
# Assumes:
#    videos are in a 'snap' directory
#    marquee are in a 'wheel' directory
#    images are in a 'boxart' directory
#
# Examples:
#        <path>./10-Yard Fight (USA, Europe).zip</path>
#        <image>./boxart/10-Yard Fight (USA, Europe).png</image>
#        <marquee>./wheel/10-Yard Fight (USA, Europe).png</marquee>
#        <video>./snap/10-Yard Fight (USA, Europe).mp4</video>
import sys
import os
import xml.etree.ElementTree as ET
import untangle
import xmltodict
import json
import getopt
import argparse
from collections import OrderedDict

def process_mega(doc):
    """Process an Sega Megadrive GameList.xml file
    Returns a list of new elements
    """
    new_elements = []

    root_elements = doc["game"] if type(doc["game"]) == list else [obj["game"]]
    for element in root_elements:
        # make all of these kid safe
        element['kidgame'] = 'true'

        #original_entries += 1
        if '(2)' in element["path"]:
            #deleted_entries += 1
            # add hidden element
            element['hidden'] = 'true'
        elif '(3)' in element["path"]:
            # add hidden element
            element['hidden'] = 'true'
            #deleted_entries += 1
        elif '(PAL)' in element["path"]:
            # add hidden element
            element['hidden'] = 'true'
            #deleted_entries += 1
        elif 'Mortal Kombat' in element["name"]:
            # add hidden element
            element['hidden'] = 'true'
            element['kidgame'] = 'false'
            #deleted_entries += 1



        new_elements.append(element)
        #print(element["path"] + '\t' +  element["name"])

    return new_elements
####### End process_mega(doc)  #################


def process_snes(doc):
    """Process an Super Nintendo Entertainment System (snes) GameList.xml file
    Returns a list of new elements
    """
    new_elements = []

    root_elements = doc["game"] if type(doc["game"]) == list else [obj["game"]]
    for element in root_elements:
        #original_entries += 1
        if '(2)' in element["path"]:
            #deleted_entries += 1
            # add hidden element
            element['hidden'] = 'true'
        elif '(3)' in element["path"]:
            # add hidden element
            element['hidden'] = 'true'
            #deleted_entries += 1
        elif '(PAL)' in element["path"]:
            # add hidden element
            element['hidden'] = 'true'
            #deleted_entries += 1

        # make all of these kid safe
        element['kidgame'] = 'true'

        new_elements.append(element)
        #print(element["path"] + '\t' +  element["name"])

    return new_elements
####### End process_snes(doc)  #################

def process_nes(doc):
    """Process an Nintendo Entertainment System (nes) GameList.xml file
    Returns a list of new elements
    """
    new_elements = []

    root_elements = doc["game"] if type(doc["game"]) == list else [obj["game"]]
    for element in root_elements:
        #original_entries += 1
        if '(2)' in element["path"]:
            #deleted_entries += 1
            # add hidden element
            element['hidden'] = 'true'
        elif '(3)' in element["path"]:
            # add hidden element
            element['hidden'] = 'true'
            #deleted_entries += 1
        elif '(PAL)' in element["path"]:
            # add hidden element
            element['hidden'] = 'true'
            #deleted_entries += 1

        # make all of these kid safe
        element['kidgame'] = 'true'

        new_elements.append(element)
        # print(element["path"] + '\t' +  element["name"])

    return new_elements
####### End process_nes(doc)  #################

def process_atari(doc):
    """Process an Atari 2600 GameList.xml file
    Returns a list of new elements
    """
    new_elements = []

    root_elements = doc["game"] if type(doc["game"]) == list else [obj["game"]]
    for element in root_elements:
        #original_entries += 1
        if '(2)' in element["path"]:
            #deleted_entries += 1
            # add hidden element
            element['hidden'] = 'true'
        elif '(3)' in element["path"]:
            # add hidden element
            element['hidden'] = 'true'
            #deleted_entries += 1
        elif '(PAL)' in element["path"]:
            # add hidden element
            element['hidden'] = 'true'
            #deleted_entries += 1

        # make all of these kid safe
        element['kidgame'] = 'true'

        new_elements.append(element)
        # print(element["path"] + '\t' +  element["name"])

    return new_elements
####### End process_atari(doc)  #################

def process_mame(doc):
    """Process an Mame 2003 GameList.xml file
        Returns a list of new elements
    """
    try:
        with open('mame-good.txt', encoding='utf-8') as fd:
            good_games = fd.read().splitlines()
    except IOError:
        print('Error: cannot find or open file for reading: ' + 'mame-good.txt')
        sys.exit(1)

    try:
        with open('mature.txt', encoding='utf-8') as fd:
            mature_games = fd.read().splitlines()
    except IOError:
        print('Error: cannot find or open file for reading: ' + 'mature.txt')
        mature_games = []
        #sys.exit(1)

    #print(mature_games)
    #print(good_games)

    new_elements = []

    root_elements = doc["game"] if type(doc["game"]) == list else [obj["game"]]
    for element in root_elements:
        # original_entries += 1
        if not element['path']:
            print("No path found, continuing.")
            continue
        if not element['name']:
            print("No name found, continuing.")
            continue
        filename = os.path.basename(os.path.normpath(element['path'])) #just the filename, not path
        filename = os.path.splitext(filename)[0]  #strip extension from filename
        if filename not in good_games:
            #print("HIDING " + filename)
            element['hidden'] = 'true'
        if filename in mature_games:
            #print("HIDING " + filename)
            element['hidden'] = 'true'
        if '(2)' in element["path"]:
            print("FOUND (2)")
            # deleted_entries += 1
            # add hidden element
            element['hidden'] = 'true'
        if '(3)' in element["path"]:
            print("FOUND (3)")
            # add hidden element
            element['hidden'] = 'true'
            # deleted_entries += 1
        if '(PAL)' in element["path"]:
            print("FOUND (PAL)")
            # add hidden element
            element['hidden'] = 'true'
            # deleted_entries += 1

        # make all of these kid safe
        element['kidgame'] = 'true'

        #check if genre element exists!
        if element["genre"]:
            #print("GENRE = " + element["genre"])
            if "Horror" in element["genre"]:
                #print("FOUND HORROR GENRE")
                element['kidgame'] = 'false'
            if "Flight Simulator" in element["genre"]:
                element['hidden'] = 'true'
            if "Racing" in element["genre"]:
                element['hidden'] = 'true'
            if "Race" in element["genre"]:
                element['hidden'] = 'true'
            if "Sports" in element["genre"]:
                element['hidden'] = 'true'
            if "Quiz" in element["genre"]:
                element['hidden'] = 'true'
            if "Casino" in element["genre"]:
                element['hidden'] = 'true'

        if element["name"]:
            if 'Mortal Kombat' in element["name"]:
                # add hidden element
                element['hidden'] = 'true'
                element['kidgame'] = 'false'
                # deleted_entries += 1

        new_elements.append(element)
        # print(element["path"] + '\t' +  element["name"])

    return new_elements
####### End process_mame(doc)  #################


def process_fba(doc):
    """Process an Final Burn Alpha GameList.xml file
        Returns a list of new elements
    """
    try:
        with open('fba-good.txt', encoding='utf-8') as fd:
            good_games = fd.read().splitlines()
    except IOError:
        print('Error: cannot find or open file for reading: ' + 'fba-good.txt')
        sys.exit(1)

    try:
        with open('mature.txt', encoding='utf-8') as fd:
            mature_games = fd.read().splitlines()
    except IOError:
        print('Error: cannot find or open file for reading: ' + 'mature.txt')
        mature_games = []
        #sys.exit(1)

    #print(mature_games)
    #print(good_games)

    new_elements = []

    root_elements = doc["game"] if type(doc["game"]) == list else [obj["game"]]
    for element in root_elements:
        # original_entries += 1
        if not element['path']:
            print("No path found, continuing.")
            continue
        if not element['name']:
            print("No name found, continuing.")
            continue
        #print("FILE: " + element['name'])
        filename = os.path.basename(os.path.normpath(element['path'])) #just the filename, not path
        filename = os.path.splitext(filename)[0]  #strip extension from filename
        if filename not in good_games:
            #print("HIDING " + filename)
            element['hidden'] = 'true'
        if filename in mature_games:
            #print("HIDING " + filename)
            element['hidden'] = 'true'
        if '(2)' in element["path"]:
            print("FOUND (2)")
            # deleted_entries += 1
            # add hidden element
            element['hidden'] = 'true'
        if '(3)' in element["path"]:
            print("FOUND (3)")
            # add hidden element
            element['hidden'] = 'true'
            # deleted_entries += 1
        if '(PAL)' in element["path"]:
            print("FOUND (PAL)")
            # add hidden element
            element['hidden'] = 'true'
            # deleted_entries += 1

        # make all of these kid safe
        element['kidgame'] = 'true'

        #check if genre element exists!
        if element["genre"]:
            #print("GENRE = " + element["genre"])
            if "Horror" in element["genre"]:
                #print("FOUND HORROR GENRE")
                element['kidgame'] = 'false'
            if "Flight Simulator" in element["genre"]:
                element['hidden'] = 'true'
            if "Racing" in element["genre"]:
                element['hidden'] = 'true'
            if "Casino" in element["genre"]:
                element['hidden'] = 'true'
            if "Electromechanical" in element["genre"]:
                element['hidden'] = 'true'
            if "Ball" in element["genre"]:
                element['hidden'] = 'true'
            if "Multi" in element["genre"]:
                element['hidden'] = 'true'
            if "Quiz" in element["genre"]:
                element['hidden'] = 'true'
            if "Rythm" in element["genre"]:
                element['hidden'] = 'true'
            if "Tabletop" in element["genre"]:
                element['hidden'] = 'true'
            if "Utilities" in element["genre"]:
                element['hidden'] = 'true'
            if "Whac" in element["genre"]:
                element['hidden'] = 'true'
            if "Slot" in element["genre"]:
                element['hidden'] = 'true'
            if "Console" in element["genre"]:
                element['hidden'] = 'true'
            if "Sports" in element["genre"]:
                element['hidden'] = 'true'

        new_elements.append(element)
        # print(element["path"] + '\t' +  element["name"])

    return new_elements
####### End process_fba(doc)  #################

def main(argv):
    infile = ''
    outfile = ''

    parser = argparse.ArgumentParser(
        description = 'Game List XML Editor for EmulationStation',
        epilog='Valid emulators: mame, fba, atari, nes, snes, mega'
    )

    parser.add_argument('infilename', action="store", help='Input Filename')
    parser.add_argument('outfilename', action="store", help='Output Filename')
    parser.add_argument('-emulator', action="store", default='mame', choices=['mame', 'atari', 'fba', 'nes', 'snes', 'mega'], help='Emulator (mame, fba. atari)')

    args = parser.parse_args()

    #print(parser.parse_args())

    infilename = args.infilename
    outfilename = args.outfilename
    emulator = args.emulator

    print('Emulator file is ', emulator)
    print ('Input file is ', infilename)
    print ('Output file is ', outfilename)



    try:
        with open(infilename, encoding='utf-8') as fd:
            doc = xmltodict.parse(fd.read(), encoding='utf-8', process_namespaces=True)
    except IOError:
        print('Error: cannot find or open file for reading: ' + infilename)
        sys.exit(1)


    #print('DOC  ' + str(doc))
    #print(newdoc)


    doc = doc["gameList"] #redfine the root
    #print(type(doc))
    #print(doc)

    original_entries = 0
    deleted_entries = 0

    if emulator == 'atari':
        new_elements = process_atari(doc)
    elif emulator == 'fba':
        new_elements = process_fba(doc)
    elif emulator == 'mame':
        new_elements = process_mame(doc)
    elif emulator == 'nes':
        new_elements = process_nes(doc)
    elif emulator == 'snes':
        new_elements = process_snes(doc)
    elif emulator == 'mega':
        new_elements = process_mega(doc)
    else:
        print("ERROR, please choose a valid emulator!")
        sys.exit(1)



    #print(new_elements)

    #newdoc = OrderedDict('gameList')
    newdoc = OrderedDict()
    newdoc['game'] = new_elements


    #newdoc['gameList'] = OrderedDict()
    #newdoc = newdoc["gameList"] #redfine the root



    #print(type(doc))

    # Output the updated list
    doc = {'root':doc} #reset the root pointer
    newdoc = {'gameList':newdoc} #reset the root pointer
    #print('NEWDOC  ' + str(newdoc))
    output_xml = xmltodict.unparse(newdoc, pretty=True)
    #print(output_xml)

    try:
        with open(outfilename, "w", encoding='utf-8') as f:
            f.write(output_xml)
    except IOError:
        print('Error: cannot open file for writing: ' + outfilename)
        sys.exit(1)

    #print (doc['gameList'])

    #mystring = json.loads(json.dumps(doc))
    #print(mystring)

    # Finally write the gamelist XML to gamelist-mod.xml
    #tree.write('gamelist-mod.xml')

    #print("Original Entries = ", original_entries)
    #print("Deleted Entries = ", deleted_entries)
    #print("Current Entries = ", original_entries - deleted_entries)

    print("Finished!")

if __name__ == "__main__":
   main(sys.argv[1:])