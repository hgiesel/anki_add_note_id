from random import choice
from string import hexdigits

from aqt import mw
from aqt.gui_hooks import (
    add_cards_will_add_note,
    add_cards_did_add_note,
)

from .utils import reduce_setting_keyword, copy_setting_keyword, reduce_value

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
    reduce = mw.col.get_config(reduce_setting_keyword, False)

    noteid = note.id - reduce_value if reduce else note.id

    for id, fld in enumerate(flds):
        if 'meta' in fld and fld['meta'] == 'noteid':
            note.fields[id] = str(noteid)

    if mw.pm.profile.get('copyNoteidToClipboard'):
        copy_to_clipboard(str(noteid))

    note.flush()

def init_addcards():
    add_cards_will_add_note.append(make_unique_for_dupe_check)
    add_cards_did_add_note.append(fill_with_noteid)
