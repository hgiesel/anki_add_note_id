from random import choice
from string import hexdigits

from aqt import mw
from aqt.gui_hooks import (
    add_cards_will_add_note,
    add_cards_did_add_note,
)

def copy_to_clipboard(text):
    mw.app.clipboard().setText(text)

def make_unique_for_dupe_check(problem, note):
    flds = note.model()['flds']

    random_string = ''.join(choice(hexdigits) for i in range(30))

    for id, fld in enumerate(flds):
        if 'meta' in fld and fld['meta'] == 'noteid':
            note.fields[id] = random_string

    ret = note.dupeOrEmpty()
    if ret != 1:
        problem = None

    return problem

def fill_with_noteid(note):
    flds = note.model()['flds']

    for id, fld in enumerate(flds):
        if 'meta' in fld and fld['meta'] == 'noteid':
            note.fields[id] = str(note.id)

    # TODO this probably deserves its own add-on
    if mw.pm.profile.get('copyNoteidToClipboard'):
        copy_to_clipboard(str(note.id))

    note.flush()

def init_addcards():
    add_cards_will_add_note.append(make_unique_for_dupe_check)
    add_cards_did_add_note.append(fill_with_noteid)
