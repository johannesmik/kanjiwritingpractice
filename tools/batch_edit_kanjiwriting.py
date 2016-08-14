# -*- coding: UTF-8 -*-

"""
This is a Anki plugin written in python.

I use it to batch edit the Kanji Writing Deck
"""

import codecs
from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *
import sys

# When redirecting system output to a console Python2 defaults to ascii
# This makes the output unicode
sys.stdout=codecs.getwriter('utf-8')(sys.stdout)

import requests

def chooseFile():
    # let the user choose a file
    userfile = u"empty"
    userfile = QFileDialog.getOpenFileName()
    return userfile

def test_file(filename):
    # Test if the file can be parsed correctly

    # Read in the file
    with  codecs.open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Line 3 has to be "begin"
    if not lines[2].startswith("begin"):
        return False

    # TODO make more checks here

    return True

def edit_kanji(kanji, field, action, value):
    ''' Edit a kanji
        Information about the process is put out to the console. Start anki from the console to view that information. 

        kanji: the kanji to edit
        field: which field to edit, "tags" to edit the tags
        action: which action to perform: {replace, append}
        value: the value 
    '''

    ids = mw.col.findCards(u"Kanji:%s" % kanji)
    if ids:
        card = mw.col.getCard(ids[0])
        note = card.note()

        if field == "tags":
            if action == "append":
                note.setTagsFromStr(note.stringTags() + " " + value)
                print "appended kanji tags to %s" % (note.stringTags())
            elif action == "replace":
                note.setTagsFromStr(value)
                print "replaced kanji tags to %s" % (note.stringTags())
        else:
            if action == "append":
                note[field] = note[field] + value
                print "appended kanji note[%s] to %s" % (field, note[field])
            elif action == "replace":
                note[field] = value
                print "replaced kanji note[%s] to %s" % (field, note[field])
        note.flush()
    else:
        print "didnt find kanji"

def main():
    userfile = chooseFile()
    showInfo("You selected file: %s\nLet's start batch processing" % (userfile))

    if not test_file(userfile):
        showInfo("There seems to be some error with your file")
        return False
    
    # Read in the file
    with codecs.open(userfile, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines[3:]:
        kanji, attribute = line.split(',', 1)
        modifier, value = attribute.split(":", 1)
        field, action = modifier.split("(", 1)
        field = field.strip()
        action = action[:-1]
        
        edit_kanji(kanji, field, action, value)

action = QAction("edit kanji writing practice deck using a file", mw)
mw.connect(action, SIGNAL("triggered()"), main)
mw.form.menuTools.addAction(action)

